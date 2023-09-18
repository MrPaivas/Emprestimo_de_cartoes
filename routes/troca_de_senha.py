from flask import Blueprint, render_template, request, flash, redirect, session

from config.config import db
from models.colaboradores import Colaboradores
from untils.check_login_docorator import precisa_logar
import bcrypt

route_pass = Blueprint("troca-senha", __name__)

@route_pass.route("/troca-senha", methods=["GET"])
@precisa_logar
def troca_senha():
    return render_template("troca-senha.html")


@route_pass.route("/troca-senha", methods=["POST"])
@precisa_logar
def trocando():
    cursor = db.session
    senha1 = request.form["senha1"]
    senha2 = request.form["senha2"]
    acha_nome = cursor.query(Colaboradores).filter_by(nome=session["user"]).first()
    if senha1 == senha2:
        acha_nome.senha = ""
        acha_nome.password_hash = bcrypt.hashpw(senha1.encode('utf-8'), bcrypt.gensalt())
        cursor.commit()
        cursor.close()
        flash("Senha atualizada com sucesso!", "success")
        return redirect("/home")
    else:
        flash("As Senhas estão diferentes!!", 'warning')
        return redirect("/troca-senha")