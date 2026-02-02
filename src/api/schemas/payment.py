from marshmallow import Schema, fields, validate


class PaymentRequestSchema(Schema):
    debt_id = fields.Int(required=True)

    amount_paid = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0.01)
    )

    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf([
            "cash",
            "bank_transfer",
            "credit_card",
            "e_wallet"
        ])
    )

    payment_date = fields.Date()


class PaymentResponseSchema(Schema):
    payment_id = fields.Int()

    debt_id = fields.Int()

    amount_paid = fields.Float()

    payment_method = fields.Str()

    payment_date = fields.Date()

    created_at = fields.DateTime()