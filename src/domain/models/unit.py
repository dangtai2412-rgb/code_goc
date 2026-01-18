class Unit:
    def __init__(self, unit_name, product_id, conversion_rate=1.0, is_base_unit=True, unit_id=None):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.product_id = product_id       # Khóa ngoại nối đến Product
        self.conversion_rate = conversion_rate
        self.is_base_unit = is_base_unit