from db import db
class ProductModel(db.Model):
    __tablename__: str = 'products'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unqiue=False, nullable=False)
    shop_id = db.Column(db.String, db.ForeignKey('shops.id'), unique=False, nullable=False)
    shop = db.relationship('ShopModel', back_populates='products')
    stock = db.Column(db.Integer)

# Path: schemas.py
