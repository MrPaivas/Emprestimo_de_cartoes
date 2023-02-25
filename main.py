from flask import Flask, request, render_template, redirect, make_response
from cartoes import db_cartoes

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', cartoes=db_cartoes)


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
    app.run(debug=True, host='192.168.1.8', port=8080)
