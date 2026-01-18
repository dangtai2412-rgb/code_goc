from marshmallow import Schema, fields

class EmployeeRequestSchema(Schema):
    employee_name = fields.Str(required=True)
    owner_id = fields.Int(required=True) # ID của BusinessOwner
    role = fields.Str()
    active_status = fields.Bool()

class EmployeeResponseSchema(Schema):
    employee_id = fields.Int()
    employee_name = fields.Str()
    owner_id = fields.Int()
    role = fields.Str()
    active_status = fields.Bool()