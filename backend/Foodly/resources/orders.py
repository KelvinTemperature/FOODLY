from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import orders
import uuid
from schemas import OrderSchema

blueprint = Blueprint('orders', __name__, description='Orders API')


@blueprint.route('/orders/<int:order_id>')
class Order(MethodView):

    @blueprint.response(200, 'Success')
    def get(self, order_id):
        """Get order by ID"""
        return orders.get(order_id)

    @blueprint.arguments(OrderSchema)
    @blueprint.response(201, 'Order successfully created')
    def post(self, order):
        """Create a new order"""
        order_id = str(uuid.uuid4())
        orders[order_id] = order
        return { 'id': order_id, **order }, 201

    @blueprint.arguments(OrderSchema)
    @blueprint.response(200, 'Order successfully updated')
    def put(self, order, order_id):
        """Update an order"""
        orders[order_id] = order
        return orders[order_id]

    @blueprint.response(204, 'Order successfully deleted')
    def delete(self, order_id):
        """Delete an order"""
        try:
            del orders[order_id]
            return '', 204
        except KeyError:
            abort(404, message='Order not found')