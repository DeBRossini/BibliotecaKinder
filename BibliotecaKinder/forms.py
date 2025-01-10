# Criar formulários do nosso site #
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from BibliotecaKinder.models import Usuario, Livro
from sqlalchemy import func


class FormLogin(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")


class FormCriarConta(FlaskForm):
    nome_completo = StringField("Nome Completo", validators=[DataRequired()])
    cargo = SelectField("Cargo", choices= [("professor", "Professor"), ("auxiliar", "Auxiliar"), ("admin", "Administrativo")], validators=[DataRequired()])
    username = StringField("Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirmacao_senha = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo('senha', message='As senhas devem coincidir.')])
    botao_confirmacao = SubmitField("Criar usuário")

    def validate_nome_completo(self, nome_completo):
        usuario = Usuario.query.filter_by(nome_completo = nome_completo.data).first()
        if usuario:
            raise ValidationError("Colaborador já cadastrado")
    
    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        
        if ' ' in username.data:
            raise ValidationError("O campo 'Usuário' não pode conter espaços.")
    
    
    def validate_username(self, senha):
        if ' ' in senha.data:
            raise ValidationError("O campo 'Senha' não pode conter espaços.")

class FormCriarLivro(FlaskForm):
    nome_livro = StringField("Nome do Livro", validators=[DataRequired()])
    descricao = StringField("Descrição da história", validators=[DataRequired()])
    autor = StringField("Nome do(a) autor(a)", validators=[DataRequired()])
    palavras_chave = StringField("Palavras-chave para pesquisa", validators=[DataRequired()], render_kw={"placeholder":"Colocar entre vírgulas"})
    capa = FileField("Foto da Capa", validators=[FileAllowed(['jpg', 'jpeg', 'png'], "Apenas imagens são permitidas!")])
    botao_confirmacao = SubmitField("Adicionar Livro")

    def validate_nome_livro(self, nome_livro):
        livro = Livro.query.filter_by(nome_livro = nome_livro.data).first()
        if livro:
            raise ValidationError("Este livro já está cadastrado")

class FormReservarLivro(FlaskForm):
    data_prevista_entrega = DateField("Quando pretende devolver?", format='%Y-%m-%d', validators=[DataRequired()])
    botao_reserva = SubmitField("Reservar")
    botao_devolucao = SubmitField("Devolver")

class FormAlterarUsuario(FlaskForm):
    nome_completo_us = SelectField('Category', choices=[])
    novo_status = SelectField("Selecione o status do colaborador", choices=[("ativo", "Ativo"), ("inativo", "Inativo")], validators=[DataRequired()])
    botao_confirmacao = SubmitField("Alterar usuário")
