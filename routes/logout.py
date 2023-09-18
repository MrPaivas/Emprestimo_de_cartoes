from flask import Blueprint, session, flash, redirect

route_logout = Blueprint("logout", __name__)

@route_logout.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logout efetuado com sucesso!", "success")
    return redirect("/")