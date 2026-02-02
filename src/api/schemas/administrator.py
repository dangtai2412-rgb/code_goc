from marshmallow import Schema, fields, validate


class AdministratorRequestSchema(Schema):
    admin_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    admin_permission = fields.Str(
        required=True,
        validate=validate.OneOf([
            "full_access",
            "manage_users",
            "manage_finance",
            "view_only"
        ])
    )


class AdministratorResponseSchema(Schema):
    admin_id = fields.Int()
    admin_name = fields.Str()
    admin_permission = fields.Str()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
