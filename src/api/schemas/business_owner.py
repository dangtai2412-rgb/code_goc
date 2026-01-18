from marshmallow import Schema, fields

class BusinessOwnerRequestSchema(Schema):
    owner_name = fields.Str(required=True)
    admin_id = fields.Int(required=True)  # Bắt buộc nhập ID của Admin
    plan_id = fields.Int(required=True)   # Bắt buộc nhập ID của Plan
    phone_number = fields.Str()
    email = fields.Email()
    account_status = fields.Str()

class BusinessOwnerResponseSchema(Schema):
    owner_id = fields.Int()
    owner_name = fields.Str()
    admin_id = fields.Int()
    plan_id = fields.Int()
    phone_number = fields.Str()
    email = fields.Str()
    account_status = fields.Str()