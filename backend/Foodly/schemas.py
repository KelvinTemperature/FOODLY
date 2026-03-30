from marshmallow import Schema, fields


class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(load_default="")
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    shop_id = fields.Int(required=True)

class ProductUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    price = fields.Float()
    quantity = fields.Int()
    shop_id = fields.Int()


class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)


class OrderUpdateSchema(Schema):
    product_id = fields.Int()
    quantity = fields.Int()


class PlainShopSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)


class ShopUpdateSchema(Schema):
    name = fields.Str()
    address = fields.Str()
    phone = fields.Str()
    email = fields.Email()


class ShopSchema(PlainShopSchema):
    products = fields.List(fields.Nested(PlainProductSchema(), dump_only=True))


class ProductSchema(PlainProductSchema):
    shop = fields.Nested(PlainShopSchema(), dump_only=True)