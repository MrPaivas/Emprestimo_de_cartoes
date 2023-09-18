from flask import Blueprint, request, session, flash, redirect
from datetime import datetime

from models.cartoes import Cartoes
from models.logs import Logs
from untils.formated_datetime import date_now
from untils.check_login_docorator import precisa_logar
from config.config import db


route_dev = Blueprint("devolver", __name__)
@route_dev.route("/devolver", methods=["POST"])
@precisa_logar
def devolver():
    cursor = db.session()
    numero = request.form["numero"]
    data_formatada = date_now()
    salva_log = (
        cursor.query(Logs)
        .filter_by(numero_cartao=numero)
        .order_by(Logs.idlogs.desc())
        .first()
    )
    try:
        acha_cartao = cursor.query(Cartoes).filter_by(idcartoes=numero).first()
        if acha_cartao:
            if acha_cartao.situacao == "Emprestado":
                acha_cartao.usuarios = ""
                acha_cartao.situacao = "Disponível"
                acha_cartao.colaborador = ""
                acha_cartao.dia = ""
                salva_log.colaborador_devol = session["user"]
                salva_log.data_devol = date_now(True)
                cursor.commit()
                flash("Cartão Devolvido com sucesso!", "success")
            else:
                flash("O cartão não consta como Emprestado!", 'warning')
        else:
            flash("Cartão não cadastrado!", 'warning')
    except SystemError as e:
        print(e)
    return redirect("/home")