from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect 

#SQLachameyをインスタンス化する
db = SQLAlchemy()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "crud.login"
login_manager.login_message = ""

#create_app関数を作る
def create_app():
  app = Flask(__name__)
  #アプリのコンフィグ設定をする
  app.config.from_envvar("APPLICATION_SETTINGS")

  #SQLALchemyとアプリを連携する
  db.init_app(app)
  #Migrateとアプリを連携する
  Migrate(app,db)
  csrf.init_app(app)

  login_manager.init_app(app)
  
  from crud import views as crud_views

  #register_blueprintを使いviewsのcrudをアプリへ登録する
  app.register_blueprint(crud_views.crud, url_prefix="/crud")

  #これから作成するauthパッケージからviewsをimportする
  from auth import views as auth_views

  #register_blueprintを使いviewsのauthをアプリへ登録する
  app.register_blueprint(auth_views.auth, url_prefix="/auth")

  return app
