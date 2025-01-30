# Criar as rotas do nosso site #
from flask import render_template, url_for, redirect, flash, request
from app import app, database, bcrypt
from app.models import Usuario, Capas, Livro, Log
from app.forms import FormAlterarLivro, FormCriarConta, FormLogin, FormCriarLivro, FormReservarLivro, FormDevolverLivro, FormAlterarUsuario
from datetime import datetime
from flask_login import login_required, current_user, login_user, logout_user
import base64
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

@app.route("/homepage", methods=["GET", "POST"])
@login_required
def home():
    usuario = Usuario.query.filter_by(username = current_user.username).first()
    capas = Capas.query.join(Livro).add_columns(Livro.id, Livro.nome_livro, Capas.imagem, Livro.status, Livro.escola).all()
    capas_formatadas = []
    for capa in capas:
        capa_base64 = base64.b64encode(capa.imagem).decode('utf-8')
        capas_formatadas.append({
            'id': capa.id,
            'nome_livro': capa.nome_livro,
            'imagem_base64': capa_base64,
            'status': capa.status,
            'escola': capa.escola
        })
    return render_template("home.html", capas = capas_formatadas, cargo=usuario.cargo)

@app.route("/reservar-livro/<id_livro>", methods=["GET", "POST"])
@login_required
def reserva(id_livro):
    livro = Livro.query.join(Capas) \
                   .add_columns(Livro.id, Livro.escola, Livro.nome_livro, Livro.descricao, Capas.imagem, Livro.status, Livro.com_colaborador) \
                   .filter(Livro.id == id_livro) \
                   .first()
    capa_base64 = base64.b64encode(livro.imagem).decode('utf-8')
    log = Log.query.filter((Log.id_do_livro == id_livro) & (Log.data_real_de_entrega.is_(None))).first()
    print(log)
    formreservarlivro = FormReservarLivro()
    formdevolverlivro = FormDevolverLivro()
    if formreservarlivro.validate_on_submit():
        database.session.query(Livro).filter_by(id=id_livro).update({"status": "Reservado", "com_colaborador": current_user.nome_completo})
        log = Log(id_do_livro = livro.id,
                  id_do_usuario = current_user.id,
                   data_alugado = datetime.now(),
                  status = "Em aberto",
                  data_previsao_de_entrega = formreservarlivro.data_prevista_entrega.data
        )
        database.session.add(log)
        database.session.commit()

    elif formdevolverlivro.validate_on_submit() and formdevolverlivro.botao_devolucao.data:
        print("Botão de devolução clicado")
        database.session.query(Livro).filter_by(id=id_livro).update({"status": "Disponível", "com_colaborador": ""})
        database.session.query(Log).filter_by(id_do_livro=Livro.id).update({"data_real_de_entrega": datetime.now(), "status": "Finalizado"})
        database.session.commit()

    return render_template("reserva.html", livro=livro, log=log, form_reserva = formreservarlivro, form_dev = formdevolverlivro, capa = capa_base64)

@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    query = request.form.get('query', '') 
    resultados = []
    if query:
        resultados = Livro.query.join(Capas).add_columns(Livro.id, Livro.nome_livro, Livro.descricao, Livro.status, Capas.imagem).filter(
            (Livro.nome_livro.ilike(f'%{query}%')) | 
            (Livro.palavras_chave.ilike(f'%{query}%')) |
            (Livro.descricao.ilike(f'%{query}%'))
            ).all()
    capas_resultado = []
    for resultado in resultados: 
        capa_base64 = base64.b64encode(resultado.imagem).decode('utf-8')
        capas_resultado.append({
            'id': resultado.id,
            'nome_livro': resultado.nome_livro,
            'descricao': resultado.descricao,
            'status': resultado.status,
            'imagem_base64': capa_base64
        })
        
    return render_template('resultado.html', capas=capas_resultado)

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

@app.route("/alt-colaboradores", methods=["GET", "POST"])
@login_required
def altcolaboradores():
    formalterarusuario = FormAlterarUsuario()
    usuarios = Usuario.query.all() 
    formalterarusuario.nome_completo_us.choices = [("", "Selecione um usuário")] + [
        (usuario.id, usuario.nome_completo) for usuario in usuarios
    ]
    if formalterarusuario.validate_on_submit():
        usuario_id = formalterarusuario.nome_completo_us.data
        usuario = Usuario.query.get(usuario_id) 
        alterar_op = formalterarusuario.alterar_op.data
        if alterar_op == "status":
            usuario.status = formalterarusuario.novo_status.data
        elif alterar_op == "nome_completo":
            usuario.nome_completo = formalterarusuario.novo_nome.data
        elif alterar_op == "senha":
            usuario.senha = bcrypt.generate_password_hash(formalterarusuario.nova_senha.data)
        elif alterar_op == "cargo":
            usuario.cargo = formalterarusuario.novo_cargo.data
        database.session.commit()
    return render_template("altCol.html", form = formalterarusuario)

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
                      status = "Disponível",
                      escola = formcriarlivro.escola.data)
        database.session.add(livro)
        database.session.commit()
        arquivo = formcriarlivro.capa.data
        if arquivo:
            imagem_binaria = arquivo.read() 
            capa = Capas(id_livro=livro.id, imagem=imagem_binaria)
            database.session.add(capa)
        database.session.commit()

        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for("adicionarlivro"))
    return render_template("addLivro.html", form=formcriarlivro)

@app.route("/alt-livro", methods=["GET", "POST"])
@login_required
def altlivro():
    formalterarlivro = FormAlterarLivro()
    livros = Livro.query.all() 
    formalterarlivro.nome_livro.choices = [("", "Selecione um livro")] + [
        (livro.id, livro.nome_livro) for livro in livros
    ]
    if formalterarlivro.validate_on_submit():
        livro_id = formalterarlivro.novo_nome.data
        livro = Livro.query.get(livro_id)
        capa = Capas.query.get(livro_id)
        alterar_op = formalterarlivro.alterar_op.data
        if alterar_op == "nome-livro":
            livro.nome_livro = formalterarlivro.novo_nome.data
        elif alterar_op == "autor":
            livro.autor = formalterarlivro.novo_autor.data
        elif alterar_op == "descricao":
            livro.descricao = formalterarlivro.nova_descricao.data
        elif alterar_op == "palavras-chave":
            livro.palavras_chave = formalterarlivro.novas_palch.data
        elif alterar_op == "capa":
            arquivo = formalterarlivro.nova_capa.data
            imagem_binaria = arquivo.read() 
            capa.imagem = imagem_binaria
    return render_template("altLivro.html", form = formalterarlivro)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("loginpage"))

@app.route('/livros-kinder', methods=['GET', 'POST'])
def livrosKinder():
    resultados = []
    resultados = Livro.query.join(Capas).add_columns(Livro.id, Livro.nome_livro, Livro.descricao, Livro.status, Capas.imagem).filter(
        (Livro.escola.ilike("kinder"))
        ).all()
    capas_resultado = []
    for resultado in resultados: 
        capa_base64 = base64.b64encode(resultado.imagem).decode('utf-8')
        capas_resultado.append({
            'id': resultado.id,
            'nome_livro': resultado.nome_livro,
            'descricao': resultado.descricao,
            'status': resultado.status,
            'imagem_base64': capa_base64
        })
    return render_template('livrosKinder.html', capas=capas_resultado)

@app.route('/livros-young', methods=['GET', 'POST'])
def livrosYoung():
    resultados = []
    resultados = Livro.query.join(Capas).add_columns(Livro.id, Livro.nome_livro, Livro.descricao, Livro.status, Capas.imagem).filter(
        (Livro.escola.ilike("young"))
        ).all()
    capas_resultado = []
    for resultado in resultados: 
        capa_base64 = base64.b64encode(resultado.imagem).decode('utf-8')
        capas_resultado.append({
            'id': resultado.id,
            'nome_livro': resultado.nome_livro,
            'descricao': resultado.descricao,
            'status': resultado.status,
            'imagem_base64': capa_base64
        })
    return render_template('livrosYoung.html', capas=capas_resultado)