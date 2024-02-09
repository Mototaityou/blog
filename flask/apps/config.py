from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': "root",
      'password':os.environ.get("MYSQL_PW"),
      'host': "127.0.0.1:3306",
      'db_name': "test"
      })

#DB接続用のインスタンスを作成
ENGINE = create_engine(
      SQLALCHEMY_DATABASE_URI,
      convert_unicode=True,
      echo=True  #SQLをログに吐き出すフラグ
)

#上記のインスタンスを使って、MYSQLとのセッションくを張ります
session = scoped_session(
      sessionmaker(
            autoflush = False,
            autocommit = False,
            bind = ENGINE,
      )
)
# Base = declarative_base()
# Base.query = session.query_property()

SECRET_KEY = os.urandom(24)
WTF_CSRF_SECRET_KEY=os.environ.get("WTF_CSRF_SECRET_KEY")

# おまじない
SQLALCHEMY_TRACK_MODIFICATIONS = False