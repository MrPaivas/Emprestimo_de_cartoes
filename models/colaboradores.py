from config.config import db


class Colaboradores(db.Model):
    idcolaboradores = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=False)
    senha = db.Column(db.String(45), nullable=False)
    password_hash = db.Column(db.VARBINARY(255), nullable=False)

    def __repr__(self):
        return '<Colaboradores %r>' % self.nome