from marshmallow import Schema, fields, validate


class OrderRequestSchema(Schema):
    customer_id = fields.Int(required=True)

    employee_id = fields.Int(required=True)

    order_date = fields.Date(required=True)

    order_status = fields.Str(
        validate=validate.OneOf([
            "pending",
            "confirmed",
            "completed",
            "cancelled"
        ])
    )

    payment_method = fields.Str(
        validate=validate.OneOf([
            "cash",
            "bank_transfer",
            "credit_card",
            "e_wallet"
        ])
    )

    total_amount = fields.Decimal(
        places=2,
        dump_only=True
    )


class OrderResponseSchema(Schema):
    order_id = fields.Int()

    customer_id = fields.Int()
    employee_id = fields.Int()

    order_date = fields.Date()

    order_status = fields.Str()

    payment_method = fields.Str()

    total_amount = fields.Float()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()