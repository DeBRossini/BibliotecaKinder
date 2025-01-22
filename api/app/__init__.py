from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from urllib.parse import quote_plus

DB_USER = "biblioteca"
DB_PASSWORD = quote_plus("4879##de")
DB_HOST =  "localhost"
DB_PORT =  "50523"
DB_NAME =  "sys"
SECRET_KEY = "f238c63c6df4c9ad67d92046de68f5c6"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SECRET_KEY'] = SECRET_KEY


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from app import routes