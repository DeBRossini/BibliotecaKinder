# Criar as rotas do nosso site #
from flask import render_template, url_for, redirect, flash, request
from datetime import datetime
from BibliotecaKinder.models import Usuario, Capas, Livro, Log
from BibliotecaKinder import app, database, bcrypt
from flask_login import login_required, current_user, login_user, logout_user
from BibliotecaKinder.forms import FormCriarConta, FormLogin, FormCriarLivro, FormReservarLivro
import os
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET", "POST"])
def loginpage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(username = formlogin.usuario.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("home"))
        else: flash("Usuário ou senha inválidos. Tente novamente.", "danger")
    return render_template("login.html", form = formlogin)

@app.route("/homepage")
@login_required
def home():
    livros = Livro.query.all()
    usuario = Usuario.query.filter_by(username = current_user.username).first()
    capas = Capas.query.join(Livro).add_columns(Livro.id, Livro.nome_livro, Capas.imagem, Livro.status).all()
    return render_template("home.html", livros = livros, capas = capas, cargo=usuario.cargo)

@app.route("/reservar-livro/<id_livro>", methods=["GET", "POST"])
@login_required
def reserva(id_livro):
    livro = Livro.query.join(Capas, Capas.id_livro == Livro.id) \
                   .join(Log, Log.id_do_livro == Livro.id) \
                   .add_columns(Livro.id, Livro.nome_livro, Livro.descricao, Capas.imagem, Livro.status, Log.id_do_usuario) \
                   .filter(Livro.id == id_livro) \
                   .first()
    print(livro) 
    formreservarlivro = FormReservarLivro()
    if formreservarlivro.validate_on_submit():
        if formreservarlivro.botao_reserva.data:
            database.session.query(Livro).filter_by(id=Livro.id).update({"status": "Reservado"})
            log = Log(id_do_livro = livro.id,
                      id_do_usario = current_user.id,
                      data_alugado = datetime.now(),
                      status = "Em aberto"
            )
            database.session.add(log)
            database.session.commit()
        elif formreservarlivro.botao_devolucao.data:
            database.session.query(Livro).filter_by(id=Livro.id).update({"status": "Disponível"})
            database.session.query(Log).filter_by(id_do_livro=Livro.id).update({"data_real_de_entrega": datetime.now(), "status": "Finalizado"})
            database.session.add(log)
            database.session.commit()

    return render_template("reserva.html", livro=livro, form = formreservarlivro)

@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    query = request.form.get('query', '') 
    resultados = []
    if query:
        resultados = Livro.query.join(Capas).add_columns(Livro.id, Livro.nome_livro, Livro.descricao, Capas.imagem).filter(
            (Livro.nome_livro.ilike(f'%{query}%')) | 
            (Livro.palavras_chave.ilike(f'%{query}%'))
            ).all()
    
    return render_template('resultado.html', capas=resultados)

@app.route("/adicionar-colaborador", methods=["GET", "POST"])
@login_required
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
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
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
