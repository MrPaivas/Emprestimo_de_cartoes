from config.config import db


class Kit(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(45), nullable=False)
    situacao = db.Column(db.String(45), nullable=False)
    usuarios = db.Column(db.String(100), nullable=False)
    colaborador = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return '<Kit %r>' % self.usuarios
    