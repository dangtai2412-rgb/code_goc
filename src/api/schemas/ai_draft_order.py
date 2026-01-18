from marshmallow import Schema, fields

class AIDraftOrderRequestSchema(Schema):
    employee_id = fields.Int(required=True)
    ai_id = fields.Int(required=True)
    customer_id = fields.Int(required=True)
    recognized_content = fields.Str(required=True)
    confirmation_status = fields.Str()
    source = fields.Str()

class AIDraftOrderResponseSchema(Schema):
    draft_id = fields.Int()
    employee_id = fields.Int()
    ai_id = fields.Int()
    customer_id = fields.Int()
    recognized_content = fields.Str()
    confirmation_status = fields.Str()
    source = fields.Str()