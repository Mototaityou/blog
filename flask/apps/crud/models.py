from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
from datetime import datetime
from flask_login import UserMixin
import pytz
from werkzeug.security import check_password_hash

from app import db, login_manager

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False) # type: ignore
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
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(300), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

