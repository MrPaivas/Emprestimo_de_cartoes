from flask import Flask, request, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/python_estacionamento"
db = SQLAlchemy(app)

class Cartoes(db.Model):
    idcartoes = db.Column(db.Integer, primary_key=True, autoincrement=True)
    situacao = db.Column(db.String(45), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    colaborador = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Cartoes %r>' % self.usuario




@app.route('/', methods=['GET'])
def index():
    busca = Cartoes.query.order_by(Cartoes.idcartoes)
    return render_template('index.html', cartoes=busca)


@app.route('/emprestar', methods=['POST'])
def emprestar():
    numero = request.form['numero']
    usuario = request.form['usuario']

    for cartao in db_cartoes:
        if cartao['numero'] == int(numero):
            cartao['situacao'] = 'Emprestado'
            cartao['usuario'] = usuario
    return redirect('/')


@app.route('/devolver', methods=['POST'])
def devolver():
    numero = request.form['numero']
    for cartao in db_cartoes:
        if cartao['numero'] == int(numero):
            cartao['situacao'] = 'Disponível'
            cartao['usuario'] = ''
    return redirect('/')


@app.route('/adicionar', methods=['POST'])
def adicionar_cartao():
    numero = request.form['numero']
    novo_cartao = {"numero": int(numero), "situacao": "Disponível", "usuario": ""}
    db_cartoes.append(novo_cartao)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='10.151.22.169', port=8080)