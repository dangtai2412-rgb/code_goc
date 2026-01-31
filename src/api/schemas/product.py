from marshmallow import Schema, fields

class ProductRequestSchema(Schema):
    # Các trường bắt buộc
    product_name = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    selling_price = fields.Decimal(required=True)
    
    # Các trường bổ sung cho giao diện mới
    stock_quantity = fields.Int(missing=0)
    sku = fields.Str(missing=None)           # Mã SKU
    cost_price = fields.Decimal(missing=0)   # Giá vốn
    category_id = fields.Int(missing=None)   # ID danh mục
    unit_id = fields.Int(missing=None)       # ID đơn vị tính

class ProductResponseSchema(Schema):
    # Định nghĩa dữ liệu trả về cho Frontend hiển thị đẹp
    id = fields.Str()          # Trả về SKU hoặc ID
    name = fields.Str()        # Tên sản phẩm
    category = fields.Str()    # Tên danh mục (Ví dụ: "Vật liệu xây dựng")
    unit = fields.Str()        # Tên đơn vị (Ví dụ: "Bao")
    stock = fields.Int()       # Số lượng tồn
    cost_price = fields.Float() # Giá vốn
    sale_price = fields.Float() # Giá bán
    
    # Giữ lại các trường cũ nếu cần tương thích ngược (tùy chọn)
    product_id = fields.Int()
    owner_id = fields.Int()