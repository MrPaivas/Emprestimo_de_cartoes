from flask import Blueprint, render_template

from models.kit_sala import Kit
from untils.check_login_docorator import precisa_logar

route_kits = Blueprint("kits", __name__)

@route_kits.route("/kits", methods=["GET"])
@precisa_logar
def kits():
    busca = Kit.query.order_by(Kit.item_id)
    return render_template("kits.html", kits=busca)