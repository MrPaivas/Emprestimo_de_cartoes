from flask import Blueprint, make_response, request
import pandas as pd
import io

from models.logs import Logs
from untils.formated_datetime import format_date


route_down = Blueprint("download", __name__)


@route_down.route("/download", methods=["POST"])
def baixar():
    data_inicio = request.form["data_ini"]
    data_fim = request.form["data_fim"]
    data_hora_ini = data_inicio + "T00:00:00"
    data_hora_fim = data_fim + "T23:59:59"
    buscas = Logs.query.filter(
        Logs.data_emprest >= data_hora_ini, Logs.data_emprest <= data_hora_fim
    ).order_by(Logs.idlogs)

    num_empres = []
    num_cartao = []
    num_user = []
    data_emp = []
    cola_emp = []
    data_dev = []
    cola_dev = []

    for busca in buscas:
        num_empres.append(busca.idlogs)
        num_cartao.append(busca.numero_cartao)
        num_user.append(busca.usuario)
        data_emp.append(format_date(busca.data_emprest))
        cola_emp.append(busca.colaborador_empresti)
        data_dev.append(format_date(busca.data_devol))
        cola_dev.append(busca.colaborador_devol)

    df = pd.DataFrame(
        {
            "Número do Emprestimo": num_empres,
            "Número do Cartão": num_cartao,
            "Usuário": num_user,
            "Data do Emprestimo": data_emp,
            "Colaborador que Emprestou": cola_emp,
            "Data da Devolução": data_dev,
            "Colaborador que Devolveu": cola_dev,
        }
    )

    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    response = make_response(output.getvalue())
    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename=emprestimos_entre_{data_inicio}_e_{data_fim}.xlsx"
    response.headers[
        "Content-type"
    ] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    
    return response
