from marshmallow import Schema, fields, validate


class SubscriptionPlanRequestSchema(Schema):
    plan_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=150)
    )

    duration = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )  # số ngày hoặc số tháng (tuỳ bạn quy ước)

    price = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0)
    )


class SubscriptionPlanResponseSchema(Schema):
    plan_id = fields.Int()

    plan_name = fields.Str()

    duration = fields.Int()

    price = fields.Float()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()