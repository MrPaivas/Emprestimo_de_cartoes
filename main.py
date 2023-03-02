from flask import Flask, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/python_estacionamento"
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
        return '<Colaboradores %r' % self.nome


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
    acha_cartao.usuarios = usuario
    acha_cartao.situacao = "Emprestado"
    acha_cartao.colaborador = session['user']
    acha_cartao.dia = data_formatada
    cursor.commit()

    return redirect('/home')


@app.route('/devolver', methods=['POST'])
@precisa_logar
def devolver():
    cursor = db.session()
    numero = request.form['numero']

    acha_cartao = cursor.query(Cartoes).filter_by(idcartoes=numero).first()
    acha_cartao.usuarios = ""
    acha_cartao.situacao = "Disponível"
    acha_cartao.colaborador = ""
    acha_cartao.dia = ""
    cursor.commit()

    return redirect('/home')


@app.route('/adicionar', methods=['POST'])
@precisa_logar
def adicionar_cartao():
    numero = request.form['numero']
    novo_cartao = Cartoes(idcartoes=numero, situacao="Disponível", usuarios="", colaborador="")
    db.session.add(novo_cartao)
    db.session.commit()
    return redirect('/home')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout efetuado com sucesso!')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.10', port=5000)
