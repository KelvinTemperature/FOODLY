from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from authz import admin_required
from models import ShopModel
from schemas import ShopSchema, ShopUpdateSchema


blueprint = Blueprint('shops', __name__, description='Shops API')


@blueprint.route('/shops/<int:shop_id>')
class Shop(MethodView):

    @blueprint.response(200, ShopSchema)
    def get(self, shop_id):
        try:
            shop = db.session.get(ShopModel, shop_id)
            if shop:
                return shop
            abort(404, message='Shop not found')
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(ShopUpdateSchema)
    @blueprint.response(200, ShopSchema)
    @admin_required
    def put(self, shop_data, shop_id):
        try:
            shop = db.session.get(ShopModel, shop_id)
            if not shop:
                abort(404, message='Shop not found')
            for key, value in shop_data.items():
                setattr(shop, key, value)
            db.session.commit()
            return shop
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.response(204)
    @admin_required
    def delete(self, shop_id):
        try:
            shop = db.session.get(ShopModel, shop_id)
            if not shop:
                abort(404, message='Shop not found')
            db.session.delete(shop)
            db.session.commit()
            return '', 204
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blueprint.route('/shops')
class ShopList(MethodView):

    @blueprint.response(200, ShopSchema(many=True))
    def get(self):
        try:
            return ShopModel.query.all()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(ShopSchema)
    @blueprint.response(201, ShopSchema)
    @admin_required
    def post(self, shop_data):
        new_shop = ShopModel(**shop_data)
        try:
            db.session.add(new_shop)
            db.session.commit()
            return new_shop
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))
