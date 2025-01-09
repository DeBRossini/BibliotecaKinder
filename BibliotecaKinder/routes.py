# Criar as rotas do nosso site #
from flask import render_template, url_for, redirect, flash
from datetime import datetime
from BibliotecaKinder.models import Usuario, Capas, Livro
from BibliotecaKinder import app, database, bcrypt
from flask_login import login_required, current_user, login_user, logout_user
from BibliotecaKinder.forms import FormCriarConta, FormLogin, FormCriarLivro
import os
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET", "POST"])
def loginpage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(username = formlogin.usuario.data).first()
        livros = Livro.query.all()
        capas = Capas.query.all()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("home", id_usuario=usuario.id, cargo=usuario.cargo))
        else: flash("Usuário ou senha inválidos. Tente novamente.", "danger")
    return render_template("login.html", form = formlogin, livros = livros, capas = capas)

@app.route("/homepage/<id_usuario>/<cargo>")
@login_required
def home(id_usuario, cargo):
    if int(id_usuario) == int(current_user.id):
        return render_template("home.html", id_usuario=current_user.id, cargo=cargo)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("home.html", usuario=usuario, cargo=cargo)

@app.route("/reservar-livro")
@login_required
def reserva():
    pass

@app.route("/adicionar-colaborador", methods=["GET", "POST"])
#@login_required
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha_criptografada = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, 
                          nome_completo = formcriarconta.nome_completo.data, 
                          cargo = formcriarconta.cargo.data, 
                          status = "ativo", 
                          senha = senha_criptografada, 
                          data_adicao = datetime.now(), 
                          data_alteracao = datetime.now())
        database.session.add(usuario)
        database.session.commit()
    else:
        print(formcriarconta.errors) 
    return render_template("criarConta.html", form=formcriarconta)

@app.route("/adicionar-livro", methods=["GET", "POST"])
@login_required
def adicionarlivro():
    formcriarlivro = FormCriarLivro()
    if formcriarlivro.validate_on_submit():
        livro = Livro(nome_livro = formcriarlivro.nome_livro.data,
                      data_adicao = datetime.now(),
                      descricao = formcriarlivro.descricao.data,
                      autor = formcriarlivro.autor.data,
                      palavras_chave = formcriarlivro.palavras_chave.data,
                      status = "Disponível")
        database.session.add(livro)
        database.session.commit()
        arquivo = formcriarlivro.capa.data
        if arquivo:
            nome_seguro = secure_filename(arquivo.filename)
            #Salvar o arquivo na pasta capas
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            #Registrar o arquivo no banco de dados
            capa = Capas(id_livro=livro.id, imagem=nome_seguro)
            database.session.add(capa)
        database.session.commit()

        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for("adicionarlivro"))
    return render_template("addLivro.html", form=formcriarlivro)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("loginpage"))
