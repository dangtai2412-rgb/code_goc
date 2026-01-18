class OrderDetail:
    def __init__(self, order_id, product_id, unit_id, order_quantity, unit_price, line_total=None):
        self.order_id = order_id           # Khóa ngoại nối đến Order
        self.product_id = product_id       # Khóa ngoại nối đến Product
        self.unit_id = unit_id             # Khóa ngoại nối đến Unit
        self.order_quantity = order_quantity
        self.unit_price = unit_price
        self.line_total = line_total or (order_quantity * unit_price)