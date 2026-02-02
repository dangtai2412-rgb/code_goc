from marshmallow import Schema, fields, validate


class BusinessOwnerRequestSchema(Schema):
    owner_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=150)
    )

    admin_id = fields.Int(required=True)
    plan_id = fields.Int(required=True)

    phone_number = fields.Str(
        validate=validate.Regexp(r"^[0-9]{9,11}$")
    )

    email = fields.Email(required=True)

    account_status = fields.Str(
        validate=validate.OneOf([
            "active",
            "inactive",
            "suspended"
        ])
    )


class BusinessOwnerResponseSchema(Schema):
    owner_id = fields.Int()
    owner_name = fields.Str()
    admin_id = fields.Int()
    plan_id = fields.Int()

    phone_number = fields.Str()
    email = fields.Str()

    account_status = fields.Str()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()