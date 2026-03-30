from db import db


class ShopModel(db.Model):
    __tablename__ = "shops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    products = db.relationship("ProductModel", back_populates="shop", lazy="select")

    def __repr__(self):
        return f"<ShopModel {self.name}>"