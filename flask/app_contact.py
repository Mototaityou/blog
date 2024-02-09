from flask_debugtoolbar import DebugToolbarExtension
from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from sqlalchemy.sql.expression import text

from werkzeug.security import generate_password_hash, check_password_hash
import logging
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
import pytz


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': "root",
      'password':os.environ["MYSQL_PW"],
      'host': "127.0.0.1:3306",
      'db_name': "test"
      })
app.config['SECRET_KEY'] = os.urandom(24)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
#ログレベルを設定する
app.logger.setLevel(logging.DEBUG)

# リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# おまじない
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Mailクラスのコンフィグを追加する
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
#flask-mail拡張を登録する
mail = Mail(app)

# DebugToolExtensionにアプリケーションをセットする
toolbar = DebugToolbarExtension(app)

# dbの初期化
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    short_content = db.Column(db.String(300), nullable=False)
    content = db.Column(db.JSON())
    created_at =db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    updated_at =db.Column(db.DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    image_path =db.Column(db.String(300), nullable=False)
    def html(self):
        return self.content['html']

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
  
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html',posts=posts)

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/edit')
    else:
        return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/create',methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        image_path = request.form.get('image_path')
        short_content =request.form.get('short_content')

        post = Post(title=title, image_path=image_path, short_content=short_content)

        db.session.add(post)
        db.session.commit()
        db.engine.execute(f"UPDATE post SET content ='{request.form.get('content')}'")
        return redirect('/edit')
    else:
        return render_template('create.html')

@app.route('/<int:id>/update',methods=['GET','POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.image_path = request.form.get('image_path')
        post.short_content =request.form.get('short_content')

        db.session.commit()
        db.engine.execute(f"UPDATE post SET content ='{request.form.get('content')}' WHERE id={id}")
        return redirect('/edit')

@app.route('/<int:id>/delete',methods=['GET'])
@login_required
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/edit')

@app.route("/about/")
def about():
    return render_template("about.html",\
        about = True, \
        title = 'about')

@app.route("/articles/")
def articles():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('articles.html',posts=posts)

@app.route('/<int:id>/articlesview/',methods=['GET','POST'])
def articlesview(id):
    if request.method == 'GET':
        posts = Post.query.get(id)
        return render_template('articlesview.html',posts=posts)

@app.route("/edit/", methods=['GET','POST'])
@login_required
def edit():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('edit.html',posts=posts)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        #form属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True

        if not username:
            flash("お名前は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect('/contact')

        #メールを送る
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username = username,
            description = description,
        )

        #contactエンドポイントへリダイレクトする
        flash("問い合わせ内容はメールにて送信致しました。問い合わせありがとうございました。")
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")

app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")

def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


