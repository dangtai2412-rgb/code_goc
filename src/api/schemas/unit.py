from marshmallow import Schema, fields

class UnitRequestSchema(Schema):
    unit_name = fields.Str(required=True)
    product_id = fields.Int(required=True)
    conversion_rate = fields.Decimal()
    is_base_unit = fields.Bool()

class UnitResponseSchema(Schema):
    unit_id = fields.Int()
    unit_name = fields.Str()
    product_id = fields.Int()
    conversion_rate = fields.Float()
    is_base_unit = fields.Bool()