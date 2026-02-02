from marshmallow import Schema, fields, validate

class OrderDetailRequestSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    unit_price = fields.Decimal(required=True)

class OrderRequestSchema(Schema):
    customer_id = fields.Int(required=True)
    # employee_id không cần gửi từ body, sẽ lấy từ Token hoặc để null
    payment_method = fields.Str(validate=validate.OneOf(["CASH", "BANK_TRANSFER", "CARD"]))
    total_amount = fields.Decimal(required=True)
    paid_amount = fields.Decimal(missing=0)
    
    # Quan trọng: Cho phép gửi danh sách chi tiết đơn hàng
    details = fields.List(fields.Nested(OrderDetailRequestSchema), required=True)

class OrderResponseSchema(Schema):
    order_id = fields.Int()
    customer_id = fields.Int()
    order_date = fields.DateTime()
    order_status = fields.Str()
    total_amount = fields.Float()
    payment_status = fields.Str()
    # Có thể thêm details vào response nếu muốn hiện chi tiết ngay