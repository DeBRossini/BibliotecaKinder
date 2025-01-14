from BibliotecaKinder.forms import FormLogin
from BibliotecaKinder.models import Usuario
from BibliotecaKinder import app, bcrypt
from flask_login import  login_user
from flask import render_template, url_for, redirect, flash

if __name__ == "__main__":
    app.run()

from BibliotecaKinder import routes

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
