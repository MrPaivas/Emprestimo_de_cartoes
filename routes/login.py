import bcrypt
from flask import Blueprint, render_template, request, session, flash, redirect, jsonify
from config.config import db

from models.colaboradores import Colaboradores

route_login = Blueprint("/", __name__)

@route_login.route("/", methods=["GET"])
def login():
    """Função que renderiza a pagina de login"""
    return render_template("index.html")


@route_login.route("/", methods=["POST"])
def autentica():
    """Função que faz a lógica do login"""
    cursor = db.session
    form_name = request.form["login"]
    form_pass = request.form["senha"]
    
    db_query = (cursor.query(Colaboradores).filter_by(nome=form_name).first())
    form_bytes_pass = bytes(form_pass.encode('utf-8'))

    if db_query:
        if form_name == db_query.nome and form_pass == db_query.senha:
            session["user"] = form_name
            flash("Senha Expirada!, atualize sua senha!", 'warning')
            return redirect("/troca-senha")

        elif db_query and bcrypt.checkpw(form_bytes_pass, db_query.password_hash):
            session["user"] = form_name
            flash(f"{form_name}, logado com sucesso!", "success")
            return redirect("/home")
    
    flash(u"Usuário ou senha incorreta.", 'warning')
    return redirect("/")


