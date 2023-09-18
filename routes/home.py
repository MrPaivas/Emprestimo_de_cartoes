from flask import Blueprint, render_template

from models.cartoes import Cartoes
from untils.check_login_docorator import precisa_logar

route_home = Blueprint("home", __name__)

@route_home.route("/home", methods=["GET"])
@precisa_logar
def index():
    busca = Cartoes.query.order_by(Cartoes.idcartoes)
    return render_template("home.html", cartoes=busca)