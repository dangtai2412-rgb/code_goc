from marshmallow import Schema, fields

class ProductRequestSchema(Schema):
    product_name = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    selling_price = fields.Decimal()
    stock_quantity = fields.Int()

class ProductResponseSchema(Schema):
    product_id = fields.Int()
    product_name = fields.Str()
    owner_id = fields.Int()
    selling_price = fields.Float()
    stock_quantity = fields.Int()