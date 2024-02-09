from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import json
load_dotenv()
from datetime import date, datetime
import pytz

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': "root",
      'password':os.environ["MYSQL_PW"],
      'host': "127.0.0.1:3306",
      'db_name': "test"
  })
# おまじない
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# dbの初期化
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    created_at =db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    updated_at =db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    image_path =db.Column(db.String(300), nullable=False)

res=db.engine.execute("SELECT * FROM goods")
print(res)
for row in res:
    print(row)

@app.route("/")
def index():
    res=db.engine.excute("SELECT * FROM posts")
    rows=[]
    for row in res:
        print(row)
        rows.append(row)
    return render_template('index.html', \
        index = True, \
        title = 'index',
        main = rows)

def content():
    res=db.engine.excute("SELECT content FROM posts")
    for row in res:
        data=json.load(row)
        print(date["html"])
    return render_template('index.html', \
        index = True, \
        title = 'index',
        html = date["html"])

if __name__=='__main__':
    app.run()

@app.route("/about/")
def about():
    return render_template("about.html",\
        about = True, \
        title = 'about')

@app.route("/articles/")
def articles():
    res=db.engine.execute("SELECT * FROM posts")
    rows=[]
    for row in res:
        print(row)
        rows.append(row)
    return render_template("articles.html",\
        articles = True, \
        title = 'articles',
        main = rows)

@app.route("/articles/<int:id>")
def articlesview(id):
    res=db.engine.execute(f"SELECT * FROM posts WHERE id={id}")
    for row in res:
        data=json.loads(row[2])
        print(data["html"])
    return render_template("articlesview.html",\
        articleview=True,
        main=row,
        html=data["html"])

@app.route("/create")
def create():
    render_template("create.html")