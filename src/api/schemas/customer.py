from marshmallow import Schema, fields

class CustomerRequestSchema(Schema):
    customer_name = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    phone_number = fields.Str()
    address = fields.Str()
    total_outstanding_debt = fields.Decimal()

class CustomerResponseSchema(Schema):
    customer_id = fields.Int()
    customer_name = fields.Str()
    owner_id = fields.Int()
    phone_number = fields.Str()
    address = fields.Str()
    total_outstanding_debt = fields.Float()