# Criar formulários do nosso site #
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from api.app.models import Usuario, Livro
from sqlalchemy import func


class FormLogin(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired()], render_kw={"placeholder":"Usuário"})
    senha = PasswordField("Senha", validators=[DataRequired()], render_kw={"placeholder":"Senha"})
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
    descricao = TextAreaField("Descrição da história", validators=[DataRequired()], render_kw={"rows":"3"})
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

class FormDevolverLivro(FlaskForm):
    botao_devolucao = SubmitField("Devolver")

class FormAlterarUsuario(FlaskForm):
    nome_completo_us = SelectField('Nome do colaborador', choices=[])
    alterar_op = SelectField('O que deseja alterar?', choices=[("","Selecione"),("status", "Status"), ("nome_completo", "Nome completo"), ("senha", "Senha"), ("cargo", "Cargo")])
    novo_status = SelectField("Selecione o status do colaborador", choices=[("ativo", "Ativo"), ("inativo", "Inativo")])
    novo_nome = StringField("Novo nome")
    nova_senha=PasswordField("Nova senha")
    novo_cargo = SelectField("Cargo", choices= [("professor", "Professor"), ("auxiliar", "Auxiliar"), ("admin", "Administrativo")])
    botao_confirmacao = SubmitField("Alterar usuário")

class FormAlterarLivro(FlaskForm):
    nome_livro = SelectField('Nome do colaborador', choices=[])
    alterar_op = SelectField('O que deseja alterar?', choices=[("","Selecione"),("nome-livro", "Nome do Livro"), ("autor", "Autor"), ("descricao", "Descrição"), ("palavras-chave", "Palavras chave")])
    novo_nome = StringField("Novo nome")
    novo_autor = StringField("Novo autor")
    nova_descricao = StringField("Nova descrição")
    novas_palch = StringField("Novas palavras-chave", render_kw={"placeholder":"Colocar entre vírgulas"})
    botao_confirmacao = SubmitField("Alterar Livro")