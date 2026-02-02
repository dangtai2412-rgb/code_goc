from marshmallow import Schema, fields, validate


class EmployeeRequestSchema(Schema):
    employee_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    owner_id = fields.Int(required=True)

    role = fields.Str(
        validate=validate.OneOf([
            "manager",
            "cashier",
            "staff",
            "accountant"
        ])
    )

    active_status = fields.Bool(missing=True)


class EmployeeResponseSchema(Schema):
    employee_id = fields.Int()

    employee_name = fields.Str()
    owner_id = fields.Int()

    role = fields.Str()
    active_status = fields.Bool()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()