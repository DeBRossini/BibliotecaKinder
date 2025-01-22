from api.app import database, app
from api.app.models import Usuario, Livro, Capas, Log

with app.app_context():
    database.create_all()