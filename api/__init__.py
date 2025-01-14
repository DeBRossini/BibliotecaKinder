from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'comunidade.db')}"
app.config['SECRET_KEY'] = "f238c63c6df4c9ad67d92056de68f5c6"
app.config["UPLOAD_FOLDER"] = "static/capas"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from api.app import routes
