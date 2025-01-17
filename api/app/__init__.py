from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from urllib.parse import quote_plus


DB_USER = os.getenv("DB_USER", "root")  
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", "4879@@de"))
DB_HOST = os.getenv("DB_HOST", "192.168.1.21") 
DB_PORT = os.getenv("DB_PORT", "3306") 
DB_NAME = os.getenv("DB_NAME", "sys")
SECRET_KEY = os.getenv("SECRET_KEY", "1")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SECRET_KEY'] = SECRET_KEY
app.config["UPLOAD_FOLDER"] = "static/capas"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from api.app import routes