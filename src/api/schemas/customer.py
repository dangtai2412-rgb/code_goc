from marshmallow import Schema, fields, validate


class CustomerRequestSchema(Schema):
    customer_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=150)
    )

    owner_id = fields.Int(required=True)

    phone_number = fields.Str(
        validate=validate.Regexp(r"^[0-9]{9,11}$")
    )

    address = fields.Str(
        validate=validate.Length(max=255)
    )

    total_outstanding_debt = fields.Decimal(
        as_string=True,
        places=2,
        required=False
    )


class CustomerResponseSchema(Schema):
    customer_id = fields.Int()
    customer_name = fields.Str()
    owner_id = fields.Int()

    phone_number = fields.Str()
    address = fields.Str()

    total_outstanding_debt = fields.Float()

    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()