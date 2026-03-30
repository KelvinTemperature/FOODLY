from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import ProductSchema, ProductUpdateSchema
from models import ProductModel


blueprint = Blueprint('products', __name__, description='Products API')

@blueprint.route('/products/<int:product_id>')
class Product(MethodView):

    @blueprint.response(200, ProductSchema)
    def get(self, product_id):
        """Get product by ID"""
        try:
            product = db.session.get(ProductModel, product_id)
            if product:
                return product

            abort(404, message='Product not found')
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(200, ProductSchema)
    def put(self, product_data, product_id):
        """Update a product"""
        try:
            product = db.session.get(ProductModel, product_id)
            if product:
                for key, value in product_data.items():
                    setattr(product, key, value)

                db.session.commit()
                return product

            abort(404, message='Product not found')
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.response(204, 'Product successfully deleted')
    def delete(self, product_id):
        """Delete a product"""
        try:
            product = db.session.get(ProductModel, product_id)
            if product:
                db.session.delete(product)
                db.session.commit()
                return '', 204

            abort(404, message='Product not found')
        except SQLAlchemyError as e:
            abort(500, message=str(e))




@blueprint.route('/products')
class ProductList(MethodView):

    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        """Get all products"""
        try:
            return ProductModel.query.all()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(ProductSchema)
    @blueprint.response(201, ProductSchema)
    def post(self, product_data):
        """Create a new product validate before creating"""

        new_product = ProductModel(**product_data)

        try:
            db.session.add(new_product)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return new_product



