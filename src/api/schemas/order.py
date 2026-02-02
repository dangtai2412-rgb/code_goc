# src/api/schemas/order.py
from marshmallow import Schema, fields, validate

# 1. Schema cho từng món hàng (Chi tiết)
class OrderDetailRequestSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1, error="Số lượng phải lớn hơn 0"))
    unit_price = fields.Decimal(required=True)

# 2. Schema cho Đơn hàng tổng (Header)
class OrderRequestSchema(Schema):
    customer_id = fields.Int(required=True)
    payment_method = fields.Str(validate=validate.OneOf(["CASH", "BANK_TRANSFER", "CARD", "DEBT"]))
    total_amount = fields.Decimal(required=True)
    paid_amount = fields.Decimal(missing=0)
    note = fields.Str(allow_none=True)
    
    # QUAN TRỌNG: Cho phép gửi kèm danh sách sản phẩm ngay khi tạo đơn
    details = fields.List(fields.Nested(OrderDetailRequestSchema), required=True, validate=validate.Length(min=1, error="Đơn hàng phải có ít nhất 1 sản phẩm"))

class OrderResponseSchema(Schema):
    order_id = fields.Int()
    customer_id = fields.Int()
    order_date = fields.DateTime()
    order_status = fields.Str()
    payment_method = fields.Str()
    total_amount = fields.Float()
    paid_amount = fields.Float()
    # Nếu muốn trả về cả chi tiết khi tạo xong, có thể bỏ comment dòng dưới
    # details = fields.Nested(OrderDetailResponseSchema, many=True)