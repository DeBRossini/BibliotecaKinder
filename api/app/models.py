# Criar a estrutura do banco de dados #

from api.app import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    nome_completo = database.Column(database.String, nullable=False, unique=True)
    cargo = database.Column(database.String,nullable=False)
    status = database.Column(database.String, nullable=False)
    senha = database.Column(database.String, nullable=False)
    data_adicao = database.Column(database.DateTime, nullable=False)
    data_alteracao = database.Column(database.DateTime, nullable=False)

class Log(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_do_livro= database.Column(database.Integer, database.ForeignKey('livro.id'), nullable=False)
    id_do_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    data_alugado = database.Column(database.DateTime, nullable=False)
    data_previsao_de_entrega = database.Column(database.DateTime)
    data_real_de_entrega = database.Column(database.DateTime)
    status = database.Column(database.String, nullable=False)

class Livro(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_livro = database.Column(database.String,nullable=False)
    data_adicao = database.Column(database.DateTime)
    descricao = database.Column(database.String,nullable=False)
    autor = database.Column(database.String,nullable=False)
    palavras_chave = database.Column(database.String,nullable=False)
    capa = database.relationship("Capas", backref= "Livro", lazy=True)
    com_colaborador = database.Column(database.String, nullable= True)
    status = database.Column(database.String,nullable=False)

class Capas(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_livro = database.Column(database.Integer, database.ForeignKey('livro.id'), nullable=False)
    imagem = database.Column(database.String, default="default.png")