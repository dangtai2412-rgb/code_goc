from marshmallow import Schema, fields, validate


class ProductRequestSchema(Schema):
    product_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    owner_id = fields.Int(required=True)

    selling_price = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0)
    )

    stock_quantity = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )


class ProductResponseSchema(Schema):
    product_id = fields.Int()

    product_name = fields.Str()

    owner_id = fields.Int()

    selling_price = fields.Float()

    stock_quantity = fields.Int()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
