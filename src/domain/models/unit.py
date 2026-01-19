class Unit:
    def __init__(self, product_id, unit_name, conversion_rate, is_base_unit=False, unit_id=None):
        self.unit_id = unit_id
        self.product_id = product_id
        self.unit_name = unit_name
        self.conversion_rate = conversion_rate
        self.is_base_unit = is_base_unit