from flask import Blueprint, request, flash, redirect

from models.cartoes import Cartoes
from models.kit_sala import Kit
from untils.check_login_docorator import precisa_logar
from config.config import db

route_add = Blueprint("adicionar", __name__)

@route_add.route("/adicionar", methods=["POST"])
@precisa_logar
def adicionar_cartao():
    cursor = db.session
    tipo_formulario = request.form.get("tipo_formulario")

    if tipo_formulario == "cartao":
        numero = request.form["numero"]
        novo_elemento = Cartoes(
            idcartoes=numero, situacao="Disponível", usuarios="", colaborador="", dia=""
        )
        acha_elemento = cursor.query(Cartoes).filter_by(idcartoes=numero).first()
    elif tipo_formulario == "kits":
        item_id_form = request.form["item_id"]
        item_nome = request.form["item_nome"]
        novo_elemento = Kit(
            item_id=item_id_form,
            item_name=item_nome,
            situacao="Disponível",
            usuarios="",
            colaborador="",
            data=""
            )
        acha_elemento = cursor.query(Kit).filter_by(item_id=item_id_form).first()
    
    if acha_elemento is None:
        cursor.add(novo_elemento)
        cursor.commit()
        flash("Adicionado com sucesso!", "success")
    else:
        flash("Já adicionado!", 'warning')
    if tipo_formulario == "cartao":
        return redirect("/home")
    elif tipo_formulario == "kits":
        return redirect("/kits")