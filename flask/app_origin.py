from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from sqlalchemy.sql.expression import text

from werkzeug.security import generate_password_hash, check_password_hash
import os
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

# おまじない
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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

@app.route("/edit/", methods=['GET','POST'])
@login_required
def edit():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('edit.html',posts=posts)

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

@app.route("/contact/")
def contact():
    return render_template("contact.html",\
        contact = True, \
        title = 'contact')

@app.route("/complete/")
def complete():
    return render_template("complete.html",\
        complete = True, \
        title = 'complete')
