from BibliotecaKinder import database, app
from BibliotecaKinder.models import Usuario, Livro, Capas, Log

with app.app_context():
    database.create_all()