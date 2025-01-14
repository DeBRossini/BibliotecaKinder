from app import database, app
from app.models import Usuario, Livro, Capas, Log

with app.app_context():
    database.create_all()
