from marshmallow import Schema, fields

class OrderDetailRequestSchema(Schema):
    order_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    unit_id = fields.Int(required=True)
    order_quantity = fields.Int(required=True)
    unit_price = fields.Decimal(required=True)
    line_total = fields.Decimal()

class OrderDetailResponseSchema(Schema):
    order_id = fields.Int()
    product_id = fields.Int()
    unit_id = fields.Int()
    order_quantity = fields.Int()
    unit_price = fields.Float()
    line_total = fields.Float()