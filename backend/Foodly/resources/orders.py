from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from authz import admin_required
from models import OrderModel, ProductModel
from payment_gateway import process_payment
from schemas import OrderCreateSchema, OrderSchema, OrderUpdateSchema

blueprint = Blueprint('orders', __name__, description='Orders API')

DELIVERY_FEES = {
    'Al Asimah': 1.0,
    'Hawalli': 1.25,
    'Farwaniya': 1.5,
    'Mubarak Al-Kabeer': 1.75,
    'Ahmadi': 2.0,
    'Jahra': 2.25,
}


def _apply_order_pricing(order, product):
    order.subtotal = round(product.price * order.quantity, 2)
    order.delivery_fee = DELIVERY_FEES.get(order.governorate, 2.0)
    order.total_amount = round(order.subtotal + order.delivery_fee, 2)


@blueprint.route('/orders/<int:order_id>')
class Order(MethodView):

    @blueprint.response(200, OrderSchema)
    def get(self, order_id):
        try:
            order = db.session.get(OrderModel, order_id)
            if not order:
                abort(404, message='Order not found')
            return order
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(OrderUpdateSchema)
    @blueprint.response(200, OrderSchema)
    @admin_required
    def put(self, order_data, order_id):
        try:
            order = db.session.get(OrderModel, order_id)
            if not order:
                abort(404, message='Order not found')

            previous_quantity = order.quantity
            previous_product_id = order.product_id

            for key, value in order_data.items():
                setattr(order, key, value)

            product = db.session.get(ProductModel, order.product_id)
            if not product:
                abort(400, message='Selected product does not exist')

            if order.product_id != previous_product_id:
                old_product = db.session.get(ProductModel, previous_product_id)
                if old_product:
                    old_product.quantity += previous_quantity
                if product.quantity < order.quantity:
                    abort(400, message='Insufficient stock for selected product')
                product.quantity -= order.quantity
            elif order.quantity != previous_quantity:
                stock_delta = order.quantity - previous_quantity
                if stock_delta > 0 and product.quantity < stock_delta:
                    abort(400, message='Insufficient stock for requested quantity')
                product.quantity -= stock_delta

            _apply_order_pricing(order, product)

            if 'payment_method' in order_data:
                payment_result = process_payment(
                    order.payment_method,
                    order.total_amount,
                    metadata={'order_id': str(order.id)},
                )
                order.payment_status = payment_result['status']
                order.payment_reference = payment_result['reference']
            db.session.commit()
            return order
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.response(204)
    @admin_required
    def delete(self, order_id):
        try:
            order = db.session.get(OrderModel, order_id)
            if not order:
                abort(404, message='Order not found')
            db.session.delete(order)
            db.session.commit()
            return '', 204
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blueprint.route('/orders')
class OrderList(MethodView):

    @blueprint.response(200, OrderSchema(many=True))
    def get(self):
        try:
            return OrderModel.query.all()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(OrderCreateSchema)
    @blueprint.response(201, OrderSchema)
    @jwt_required(optional=True)
    def post(self, order_data):
        try:
            product = db.session.get(ProductModel, order_data['product_id'])
            if not product:
                abort(400, message='Selected product does not exist')

            if product.quantity < order_data['quantity']:
                abort(400, message='Insufficient stock for requested quantity')

            new_order = OrderModel(**order_data)
            new_order.order_status = 'confirmed'
            _apply_order_pricing(new_order, product)

            identity = get_jwt_identity()
            if identity:
                new_order.user_id = int(identity)

            payment_result = process_payment(
                new_order.payment_method,
                new_order.total_amount,
                metadata={'product_id': str(new_order.product_id), 'quantity': str(new_order.quantity)},
            )
            new_order.payment_status = payment_result['status']
            new_order.payment_reference = payment_result['reference']
            product.quantity -= new_order.quantity

            db.session.add(new_order)
            db.session.commit()
            return new_order
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))
