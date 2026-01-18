from marshmallow import Schema, fields

class AdministratorRequestSchema(Schema):
    admin_name = fields.Str(required=True)
    admin_permission = fields.Str() # Quan trọng: Phải có dòng này

class AdministratorResponseSchema(Schema):
    admin_id = fields.Int()
    admin_name = fields.Str()
    admin_permission = fields.Str()