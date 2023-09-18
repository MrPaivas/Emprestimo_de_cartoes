from config.config import db


class Cartoes(db.Model):
    idcartoes = db.Column(db.Integer, primary_key=True, autoincrement=True)
    situacao = db.Column(db.String(45), nullable=False)
    usuarios = db.Column(db.String(100), nullable=False)
    colaborador = db.Column(db.String(100), nullable=False)
    dia = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return '<Cartoes %r>' % self.usuarios