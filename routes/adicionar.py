from flask import Blueprint, request, flash, redirect

from models.cartoes import Cartoes
from untils.check_login_docorator import precisa_logar
from config.config import db

route_add = Blueprint("adicionar", __name__)

@route_add.route("/adicionar", methods=["POST"])
@precisa_logar
def adicionar_cartao():
    cursor = db.session
    numero = request.form["numero"]
    novo_cartao = Cartoes(
        idcartoes=numero, situacao="Disponível", usuarios="", colaborador="", dia=""
    )
    acha_cartao = cursor.query(Cartoes).filter_by(idcartoes=numero).first()
    if acha_cartao is None:
        cursor.add(novo_cartao)
        cursor.commit()
        flash("Novo Cartão adicionado com sucesso!", "success")
    else:
        flash("Cartão já adicionado!", 'warning')
    return redirect("/home")