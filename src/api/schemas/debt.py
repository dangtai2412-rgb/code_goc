from marshmallow import Schema, fields

class DebtRequestSchema(Schema):
    order_id = fields.Int(required=True)
    customer_id = fields.Int(required=True)
    debt_amount = fields.Decimal(required=True)
    debt_status = fields.Str()
    debt_created_date = fields.Date()

class DebtResponseSchema(Schema):
    debt_id = fields.Int()
    debt_amount = fields.Float()
    debt_status = fields.Str()