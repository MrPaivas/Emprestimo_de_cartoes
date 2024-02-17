import os
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
    route_pass,
    route_kits
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
app.register_blueprint(route_kits)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
