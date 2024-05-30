from db import db

class ShopModel(db.Model):
    __tablename__: str = 'shops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    products = db.relationship('ProductModel', back_populates='shop' ,lazy='dynamic')

    def __repr__(self):
        return f'<ShopModel {self.name}>'

ShopModel.query.get()
ShopModel.query.get_or_404()