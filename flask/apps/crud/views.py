from app import db
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from crud.models import Post

#Blueprintでcrudアプリを生成する
crud = Blueprint(
  "crud", __name__, template_folder="templates",
  static_folder="static",
)

@crud.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('crud/index.html',posts=posts)

@crud.route('/create',methods=['GET','POST'])
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
        return redirect(url_for('crud.edit'))
    else:
        return render_template('/crud/create.html')

@crud.route('/<int:id>/update',methods=['GET','POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('crud/update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.image_path = request.form.get('image_path')
        post.short_content =request.form.get('short_content')

        db.session.commit()
        db.engine.execute(f"UPDATE post SET content ='{request.form.get('content')}' WHERE id={id}")
        return redirect(url_for('crud.edit'))

@crud.route('/<int:id>/delete',methods=['GET'])
@login_required
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('crud.edit'))

@crud.route("/edit/", methods=['GET','POST'])
@login_required
def edit():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('crud/edit.html',posts=posts)

@crud.route("/about/")
def about():
    return render_template("/crud/about.html",\
        about = True, \
        title = 'about')

@crud.route("/articles/")
def articles():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('crud/articles.html',posts=posts)

@crud.route('/<int:id>/articlesview/',methods=['GET','POST'])
def articlesview(id):
    if request.method == 'GET':
        posts = Post.query.get(id)
        return render_template('crud/articlesview.html',posts=posts, id=id)

@crud.route("/contact/")
def contact():
    return render_template("crud/contact.html",\
        contact = True, \
        title = 'contact')

@crud.route("/complete/")
def complete():
    return render_template("crud/complete.html",\
        complete = True, \
        title = 'complete')
