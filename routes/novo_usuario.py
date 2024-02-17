from flask import Blueprint, render_template, request, flash, redirect, session

from config.config import db
from models.colaboradores import Colaboradores
from untils.check_login_docorator import precisa_logar
import bcrypt

route_new_user = Blueprint("novo-usuario", __name__)

@route_new_user.route("/novo-usuario", methods=["GET"])
@precisa_logar
def novo_user():
    return render_template("novo-usuario.html")


@route_new_user.route("/novo-usuario", methods=["POST"])
@precisa_logar
def criando():
    nome = request.form["nome"]
    senha1 = request.form["senha1"]
    senha2 = request.form["senha2"]
    
    # Verifica se já existe um usuário com o mesmo nome
    usuario_existente = db.session.query(Colaboradores).filter_by(nome=nome).first()
    if usuario_existente:
        flash("Já existe um usuário com esse nome!", "warning")
        return redirect("/novo-usuario")
    
    if senha1 == senha2:
        # Cria um novo usuário
        novo_usuario = Colaboradores(nome=nome, senha="", password_hash=bcrypt.hashpw(senha1.encode('utf-8'), bcrypt.gensalt()))
        
        # Adiciona o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Usuário criado com sucesso!", "success")
        return redirect("/home")
    else:
        flash("As senhas estão diferentes!", "warning")
        return redirect("/novo-usuario")