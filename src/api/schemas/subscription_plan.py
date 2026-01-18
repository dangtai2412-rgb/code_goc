from marshmallow import Schema, fields

class SubscriptionPlanRequestSchema(Schema):
    plan_name = fields.Str(required=True)
    duration = fields.Int()
    price = fields.Decimal(as_string=True)

class SubscriptionPlanResponseSchema(Schema):
    plan_id = fields.Int()
    plan_name = fields.Str()
    duration = fields.Int()
    price = fields.Float()