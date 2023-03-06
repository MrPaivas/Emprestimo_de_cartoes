from flask import Flask, request, render_template, redirect, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime
import pandas as pd
import io

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/python_estacionamento"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'coconut'


def precisa_logar(f):
    @wraps(f)
    def funcao_decorativa(*args, **kwargs):
        if 'user' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return funcao_decorativa


class Cartoes(db.Model):
    idcartoes = db.Column(db.Integer, primary_key=True, autoincrement=True)
    situacao = db.Column(db.String(45), nullable=False)
    usuarios = db.Column(db.String(100), nullable=False)
    colaborador = db.Column(db.String(100), nullable=False)
    dia = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return '<Cartoes %r>' % self.usuarios


class Colaboradores(db.Model):
    idcolaboradores = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=False)
    senha = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return '<Colaboradores %r>' % self.nome


class Logs(db.Model):
    idlogs = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_cartao = db.Column(db.String(45), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    data_emprest = db.Column(db.String(45), nullable=False)
    colaborador_empresti = db.Column(db.String(100), nullable=False)
    data_devol = db.Column(db.String(45), nullable=False)
    colaborador_devol = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Logs %r>' % self.idlogs


@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/autentica', methods=['POST'])
def autentica():
    cursor = db.session
    nome = request.form['login']
    senha_form = request.form['senha']
    busca_user = cursor.query(Colaboradores).filter_by(nome=nome).first()
    if senha_form == busca_user.senha:
        session['user'] = request.form['login']
        flash(session['user'] + ' logado com sucesso!')
        cursor.commit()
        return redirect('/home')
    else:
        flash('Usuário ou senha incorreta.')
        return redirect('/')


@app.route('/home', methods=['GET'])
@precisa_logar
def index():
    busca = Cartoes.query.order_by(Cartoes.idcartoes)
    return render_template('index.html', cartoes=busca)


@app.route('/emprestar', methods=['POST'])
@precisa_logar
def emprestar():
    cursor = db.session()
    numero = request.form['numero']
    usuario = request.form['usuario']
    data_hora = datetime.now()
    data_formatada = data_hora.strftime("%d/%m/%Y %H:%M:%S")

    acha_cartao = cursor.query(Cartoes).filter_by(idcartoes=numero).first()
    try:
        if acha_cartao.situacao == "Disponível":
            acha_cartao.usuarios = usuario
            acha_cartao.situacao = "Emprestado"
            acha_cartao.colaborador = session['user']
            acha_cartao.dia = data_formatada

            salva_logs = Logs(numero_cartao=numero, usuario=usuario, data_emprest=data_formatada,
                            colaborador_empresti=session['user'], data_devol="", colaborador_devol="")
            cursor.add(salva_logs)
            cursor.commit()
            flash("Cartão emprestado com sucesso!")
        else:
            flash("Cartão já emprestado! Por favor escolha outro cartão!")
    except:
        flash("Cartao nao existe")

    return redirect('/home')


@app.route('/devolver', methods=['POST'])
@precisa_logar
def devolver():
    cursor = db.session()
    numero = request.form['numero']
    acha_cartao = cursor.query(Cartoes).filter_by(idcartoes=numero).first()
    data_hora = datetime.now()
    data_formatada = data_hora.strftime("%d/%m/%Y %H:%M:%S")
    salva_log = cursor.query(Logs).filter_by(numero_cartao=numero).order_by(Logs.idlogs.desc()).first()
    if acha_cartao.situacao == "Emprestado":
        acha_cartao.usuarios = ""
        acha_cartao.situacao = "Disponível"
        acha_cartao.colaborador = ""
        acha_cartao.dia = ""
        salva_log.colaborador_devol = session['user']
        salva_log.data_devol = data_formatada
        cursor.commit()
        flash("Cartão Devolvido com sucesso!")
    else:
        flash("O cartão não consta como Emprestado!")

    return redirect('/home')


@app.route('/adicionar', methods=['POST'])
@precisa_logar
def adicionar_cartao():
    cursor = db.session
    numero = request.form['numero']
    novo_cartao = Cartoes(idcartoes=numero, situacao="Disponível", usuarios="", colaborador="", dia="")
    acha_cartao = cursor.query(Cartoes).filter_by(idcartoes=numero).first()
    if acha_cartao is None:
        cursor.add(novo_cartao)
        cursor.commit()
        flash("Novo Cartão adicionado com sucesso!")
    else:
        flash('Cartão já adicionado!')
    return redirect('/home')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout efetuado com sucesso!')
    return redirect('/')


@app.route('/download', methods=['GET'])
def baixar():

    buscas = Logs.query.order_by(Logs.idlogs)

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
        data_emp.append(busca.data_emprest)
        cola_emp.append(busca.colaborador_empresti)
        data_dev.append(busca.data_devol)
        cola_dev.append(busca.colaborador_devol)

    df = pd.DataFrame({
        'Número do Emprestimo': num_empres,
        'Número do Cartão': num_cartao,
        'Usuário': num_user,
        'Data do Emprestimo': data_emp,
        'Colaborador que Emprestou': cola_emp,
        'Data da Devolução': data_dev,
        'Colaborador que Devolveu': cola_dev})


    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)


    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=historico_emprestimos.xlsx"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response


if __name__ == '__main__':
    app.run(debug=True)
