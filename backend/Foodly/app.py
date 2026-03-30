import os

from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

import models
from db import db
from resources.orders import blueprint as orders_blueprint
from resources.products import blueprint as products_blueprint
from resources.shops import blueprint as shops_blueprint


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Foodly API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.25.2"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)
    db.init_app(app)

    api = Api(app)
    api.register_blueprint(products_blueprint)
    api.register_blueprint(shops_blueprint)
    api.register_blueprint(orders_blueprint)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)