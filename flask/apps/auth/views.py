from app import db
from auth.forms import SignUpForm, LoginForm
from crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user

#Blueprintを使ってauthを生成する
auth = Blueprint(
  "auth",
  __name__,
  template_folder="templates",
  static_folder="static"
)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        password = request.form.get('password',None)
        
        user = User(username=username, email=email, password=generate_password_hash(password, method='sha256')) # type: ignore
        
        db.session.add(user)
        db.session.commit()

        login_user(user)

        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("crud.index"):
            next_ = url_for("auth.login")
        return redirect(next_)

    return render_template('auth/signup.html', form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = request.form.get('password')

        #ユーザーが存在し、パスワードが一致する場合はログインを許可する
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("crud.edit"))

        #ログイン失敗メッセージを設定する
        flash("メールアドレスかパスワードが不正です")
    return render_template("auth/login.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))