from marshmallow import Schema, fields, validate


class DebtRequestSchema(Schema):
    order_id = fields.Int(required=True)
    customer_id = fields.Int(required=True)

    debt_amount = fields.Decimal(
        required=True,
        as_string=True,
        places=2
    )

    debt_status = fields.Str(
        validate=validate.OneOf([
            "unpaid",
            "partial",
            "paid"
        ])
    )

    debt_created_date = fields.Date(required=True)


class DebtResponseSchema(Schema):
    debt_id = fields.Int()

    order_id = fields.Int()
    customer_id = fields.Int()

    debt_amount = fields.Float()
    debt_status = fields.Str()

    debt_created_date = fields.Date()
    last_updated = fields.DateTime()