from marshmallow import Schema, fields, validate


GOVERNORATES = [
    'Al Asimah',
    'Hawalli',
    'Farwaniya',
    'Mubarak Al-Kabeer',
    'Ahmadi',
    'Jahra',
]

PAYMENT_METHODS = ['cash_on_delivery', 'knet', 'visa', 'mastercard', 'apple_pay']
PAYMENT_STATUSES = ['pending', 'authorized', 'paid', 'failed']
ORDER_STATUSES = ['confirmed', 'preparing', 'on_the_way', 'delivered', 'cancelled']

class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)

class ProductSchema(PlainProductSchema):
    shop_id = fields.Int(required=True)
    shop = fields.Nested(lambda: PlainShopSchema(), dump_only=True)

class ProductUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    price = fields.Float()
    quantity = fields.Int()

class PlainShopSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Str(required=True)

class ShopSchema(PlainShopSchema):
    products = fields.List(fields.Nested(PlainProductSchema(), dump_only=True))

class ShopUpdateSchema(Schema):
    name = fields.Str()
    address = fields.Str()
    phone = fields.Str()
    email = fields.Str()

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    user_id = fields.Int(dump_only=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    customer_name = fields.Str(required=True)
    customer_phone = fields.Str(required=True)
    customer_email = fields.Email(load_default=None, allow_none=True)
    delivery_address = fields.Str(required=True)
    governorate = fields.Str(required=True, validate=validate.OneOf(GOVERNORATES))
    payment_method = fields.Str(required=True, validate=validate.OneOf(PAYMENT_METHODS))
    payment_reference = fields.Str(dump_only=True)
    payment_status = fields.Str(dump_only=True)
    order_status = fields.Str(dump_only=True)
    subtotal = fields.Float(dump_only=True)
    delivery_fee = fields.Float(dump_only=True)
    total_amount = fields.Float(dump_only=True)
    notes = fields.Str(load_default=None, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    product = fields.Nested(PlainProductSchema(), dump_only=True)

class OrderCreateSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    customer_name = fields.Str(load_default='Guest Customer')
    customer_phone = fields.Str(load_default='+96500000000')
    customer_email = fields.Email(load_default=None, allow_none=True)
    delivery_address = fields.Str(load_default='Kuwait City')
    governorate = fields.Str(load_default='Al Asimah', validate=validate.OneOf(GOVERNORATES))
    payment_method = fields.Str(load_default='cash_on_delivery', validate=validate.OneOf(PAYMENT_METHODS))
    notes = fields.Str(load_default=None, allow_none=True)

class OrderUpdateSchema(Schema):
    product_id = fields.Int()
    quantity = fields.Int(validate=validate.Range(min=1))
    customer_name = fields.Str()
    customer_phone = fields.Str()
    customer_email = fields.Email(allow_none=True)
    delivery_address = fields.Str()
    governorate = fields.Str(validate=validate.OneOf(GOVERNORATES))
    payment_method = fields.Str(validate=validate.OneOf(PAYMENT_METHODS))
    payment_status = fields.Str(validate=validate.OneOf(PAYMENT_STATUSES))
    order_status = fields.Str(validate=validate.OneOf(ORDER_STATUSES))
    notes = fields.Str(allow_none=True)


class UserRegisterSchema(Schema):
    full_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(load_default=None, allow_none=True)
    role = fields.Str(load_default='customer', validate=validate.OneOf(['customer', 'admin']))
    password = fields.Str(required=True, validate=validate.Length(min=8))


class AuthLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class AuthUserSchema(Schema):
    id = fields.Int(required=True)
    full_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(allow_none=True)
    role = fields.Str(required=True)


class AuthResponseSchema(Schema):
    access_token = fields.Str(required=True)
    user = fields.Nested(AuthUserSchema, required=True)


class AdminRoleUpdateSchema(Schema):
    role = fields.Str(required=True, validate=validate.OneOf(['customer', 'admin']))
