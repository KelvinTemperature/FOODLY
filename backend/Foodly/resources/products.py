from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from authz import admin_required
from models import ProductModel
from schemas import ProductSchema, ProductUpdateSchema


blueprint = Blueprint('products', __name__, description='Products API')


@blueprint.route('/products/<int:product_id>')
class Product(MethodView):

    @blueprint.response(200, ProductSchema)
    def get(self, product_id):
        try:
            product = db.session.get(ProductModel, product_id)
            if product:
                return product
            abort(404, message='Product not found')
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(200, ProductSchema)
    @admin_required
    def put(self, product_data, product_id):
        try:
            product = db.session.get(ProductModel, product_id)
            if not product:
                abort(404, message='Product not found')
            for key, value in product_data.items():
                setattr(product, key, value)
            db.session.commit()
            return product
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.response(204)
    @admin_required
    def delete(self, product_id):
        try:
            product = db.session.get(ProductModel, product_id)
            if not product:
                abort(404, message='Product not found')
            db.session.delete(product)
            db.session.commit()
            return ''
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blueprint.route('/products')
class ProductList(MethodView):

    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        try:
            return ProductModel.query.all()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(ProductSchema)
    @blueprint.response(201, ProductSchema)
    @admin_required
    def post(self, product_data):
        new_product = ProductModel(**product_data)
        try:
            db.session.add(new_product)
            db.session.commit()
            return new_product
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))
