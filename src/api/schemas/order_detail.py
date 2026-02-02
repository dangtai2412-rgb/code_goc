from marshmallow import Schema, fields, validate


class OrderDetailRequestSchema(Schema):
    order_id = fields.Int(required=True)

    product_id = fields.Int(required=True)

    unit_id = fields.Int(required=True)

    order_quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    unit_price = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0)
    )

    line_total = fields.Decimal(
        places=2,
        dump_only=True
    )


class OrderDetailResponseSchema(Schema):
    order_detail_id = fields.Int()

    order_id = fields.Int()
    product_id = fields.Int()
    unit_id = fields.Int()

    order_quantity = fields.Int()
    unit_price = fields.Float()
    line_total = fields.Float()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
