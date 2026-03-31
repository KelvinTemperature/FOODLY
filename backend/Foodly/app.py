import os
from sqlalchemy import inspect, text

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_smorest import Api

import models
from db import db
from models import ProductModel, ShopModel
from resources.orders import blueprint as orders_blueprint
from resources.products import blueprint as products_blueprint
from resources.shops import blueprint as shops_blueprint
from resources.auth import blueprint as auth_blueprint
from resources.admin import blueprint as admin_blueprint
from models import UserModel


def _ensure_user_role_column():
    inspector = inspect(db.engine)
    user_columns = {column['name'] for column in inspector.get_columns('users')}
    if 'role' not in user_columns:
        db.session.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'customer'"))
        db.session.commit()


def _bootstrap_admin_account():
    admin_email = os.environ.get('FOODLY_ADMIN_EMAIL', 'givens.abraham@gmail.com').strip().lower()
    admin_password = os.environ.get('FOODLY_ADMIN_PASSWORD', 'Admin@12345')
    admin_name = os.environ.get('FOODLY_ADMIN_NAME', 'Givforks')

    existing_admin = UserModel.query.filter_by(email=admin_email).first()
    if existing_admin:
        existing_admin.role = 'admin'
        existing_admin.full_name = admin_name
        existing_admin.phone = os.environ.get('FOODLY_ADMIN_PHONE', '+96567778899')
        existing_admin.set_password(admin_password)
        db.session.commit()
        return

    admin_user = UserModel(
        full_name=admin_name,
        email=admin_email,
        phone=os.environ.get('FOODLY_ADMIN_PHONE', '+96567778899'),
        role='admin',
    )
    admin_user.set_password(admin_password)
    db.session.add(admin_user)
    db.session.commit()


def create_app():
    app = Flask(__name__)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'Foodly API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_VERSION'] = '3.25.2'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///foodly_kw.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'JWT_SECRET_KEY',
        'foodly-dev-secret-key-with-32-plus-chars',
    )

    CORS(app)
    JWTManager(app)
    db.init_app(app)

    api = Api(app)
    api.register_blueprint(products_blueprint)
    api.register_blueprint(shops_blueprint)
    api.register_blueprint(orders_blueprint)
    api.register_blueprint(auth_blueprint)
    api.register_blueprint(admin_blueprint)

    @app.get('/health')
    def health():
        return {'status': 'ok', 'service': 'foodly-api-kuwait'}

    @app.get('/catalog')
    def catalog():
        shops = ShopModel.query.all()
        products = ProductModel.query.all()
        return jsonify(
            {
                'currency': 'KWD',
                'country': 'Kuwait',
                'shops': [
                    {
                        'id': shop.id,
                        'name': shop.name,
                        'address': shop.address,
                        'phone': shop.phone,
                        'email': shop.email,
                    }
                    for shop in shops
                ],
                'products': [
                    {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'quantity': product.quantity,
                        'shop_id': product.shop_id,
                    }
                    for product in products
                ],
            }
        )

    with app.app_context():
        db.create_all()
        _ensure_user_role_column()
        _bootstrap_admin_account()

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
