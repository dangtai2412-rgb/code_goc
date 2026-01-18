from marshmallow import Schema, fields

class PaymentRequestSchema(Schema):
    debt_id = fields.Int(required=True)
    amount_paid = fields.Decimal(required=True)
    payment_method = fields.Str(required=True)
    payment_date = fields.Date()

class PaymentResponseSchema(Schema):
    payment_id = fields.Int()
    amount_paid = fields.Float()
    payment_date = fields.Date()