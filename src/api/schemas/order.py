from marshmallow import Schema, fields

class OrderRequestSchema(Schema):
    customer_id = fields.Int(required=True)
    employee_id = fields.Int(required=True)
    order_date = fields.Date(required=True)
    order_status = fields.Str()
    payment_method = fields.Str()
    total_amount = fields.Decimal()

class OrderResponseSchema(Schema):
    order_id = fields.Int()
    customer_id = fields.Int()
    employee_id = fields.Int()
    order_date = fields.Date()
    order_status = fields.Str()
    payment_method = fields.Str()
    total_amount = fields.Float()