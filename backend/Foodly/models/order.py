from db import db


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(120), nullable=False, default='Guest Customer')
    customer_phone = db.Column(db.String(50), nullable=False, default='+96500000000')
    customer_email = db.Column(db.String(120), nullable=True)
    delivery_address = db.Column(db.String(255), nullable=False, default='Kuwait City')
    governorate = db.Column(db.String(50), nullable=False, default='Al Asimah')
    payment_method = db.Column(db.String(30), nullable=False, default='cash_on_delivery')
    payment_reference = db.Column(db.String(120), nullable=True)
    payment_status = db.Column(db.String(30), nullable=False, default='pending')
    order_status = db.Column(db.String(30), nullable=False, default='confirmed')
    subtotal = db.Column(db.Float, nullable=False, default=0.0)
    delivery_fee = db.Column(db.Float, nullable=False, default=0.0)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    product = db.relationship('ProductModel', back_populates='orders')
    user = db.relationship('UserModel', back_populates='orders')
