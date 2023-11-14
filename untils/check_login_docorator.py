from flask import session, redirect
from functools import wraps

def precisa_logar(f):
    """função decoradora"""
    @wraps(f)
    def funcao_decorativa(*args, **kwargs):
        """Chamamos essa função decorada com wraps da bibli Functools que retorna para página de login"""
        if "user" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return funcao_decorativa