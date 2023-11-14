from flask import Blueprint, request, session, flash, redirect
from datetime import datetime

from models.cartoes import Cartoes
from models.logs import Logs
from untils.formated_datetime import date_now
from untils.check_login_docorator import precisa_logar
from config.config import db

route_emp = Blueprint('emprestar', __name__)


@route_emp.route("/emprestar", methods=["POST"])
@precisa_logar
def emprestar():
    cursor = db.session()
    numero = request.form["numero"]
    usuario = request.form["usuario"]
    data = date_now()
    try:
        acha_cartao = cursor.query(Cartoes).filter_by(idcartoes=numero).first()
        if acha_cartao:
            if acha_cartao.situacao == "Disponível":
                acha_cartao.usuarios = usuario
                acha_cartao.situacao = "Emprestado"
                acha_cartao.colaborador = session["user"]
                acha_cartao.dia = data

                salva_logs = Logs(
                    numero_cartao=numero,
                    usuario=usuario,
                    data_emprest=date_now(True),
                    colaborador_empresti=session["user"],
                    data_devol="",
                    colaborador_devol="",
                )
                cursor.add(salva_logs)
                cursor.commit()
                flash("Cartão emprestado com sucesso!", "success")
            else:
                flash("Cartão já emprestado! Por favor escolha outro cartão!", 'warning')
        else:
            flash("Cartão não cadastrado!", 'warning')
    except BaseExceptionGroup as e:
        print(e)
    
    return redirect("/home")