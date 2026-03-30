from db import db


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)

    shop = db.relationship("ShopModel", back_populates="products")
    orders = db.relationship("OrderModel", back_populates="product", lazy="select")
