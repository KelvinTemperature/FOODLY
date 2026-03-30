from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import OrderModel
from schemas import OrderSchema, OrderUpdateSchema

blueprint = Blueprint('orders', __name__, description='Orders API')


@blueprint.route('/orders/<int:order_id>')
class Order(MethodView):

    @blueprint.response(200, OrderSchema)
    def get(self, order_id):
        """Get order by ID"""
        try:
            order = db.session.get(OrderModel, order_id)
            if not order:
                abort(404, message='Order not found')

            return order
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(OrderUpdateSchema)
    @blueprint.response(200, OrderSchema)
    def put(self, order_data, order_id):
        """Update an order"""
        try:
            order = db.session.get(OrderModel, order_id)
            if not order:
                abort(404, message='Order not found')

            for key, value in order_data.items():
                setattr(order, key, value)

            db.session.commit()
            return order
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.response(204, 'Order successfully deleted')
    def delete(self, order_id):
        """Delete an order"""
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
        """Get all orders"""
        try:
            return OrderModel.query.all()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blueprint.arguments(OrderSchema)
    @blueprint.response(201, OrderSchema)
    def post(self, order_data):
        """Create a new order"""
        new_order = OrderModel(**order_data)

        try:
            db.session.add(new_order)
            db.session.commit()
            return new_order
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))