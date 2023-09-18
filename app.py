from flask import Flask
from config.config import Config, db

from routes import (
    route_emp,
    route_home,
    route_login,
    route_add,
    route_dev,
    route_down,
    route_logout,
    route_pass
    )


app = Flask(__name__)
app.config.from_object(Config())
db.init_app(app)

app.register_blueprint(route_emp)
app.register_blueprint(route_home)
app.register_blueprint(route_login)
app.register_blueprint(route_add)
app.register_blueprint(route_dev)
app.register_blueprint(route_down)
app.register_blueprint(route_logout)
app.register_blueprint(route_pass)

if __name__ == "__main__":
    app.run(
        host='192.168.1.25',
        port=443,  # Porta padrão HTTPS é 443
        ssl_context=('./cert/cert.pem', './cert/key.pem')  # Certificado e chave privada
    )