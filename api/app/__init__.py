from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from urllib.parse import quote_plus
import pymysql

pymysql.install_as_MySQLdb()

DB_USER = "db_kinder"
DB_PASSWORD = quote_plus("Loca@102030")
DB_HOST = "db_kinder.mysql.dbaas.com.br"
DB_NAME = "db_kinder"
SECRET_KEY = "f238c63c6df4c9ad67d92046de68f5c6"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?connect_timeout=30"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 300,
    'pool_pre_ping': True,
    'pool_timeout': 30,
    'max_overflow': 10
}

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from api.app import routes
