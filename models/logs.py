from config.config import db


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
