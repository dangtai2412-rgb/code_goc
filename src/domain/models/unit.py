# src/domain/models/unit.py
class Unit:
    def __init__(self, unit_name, description=None, owner_id=None, product_id=None, conversion_rate=1.0, is_base_unit=True, unit_id=None):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.description = description
        self.owner_id = owner_id
        self.product_id = product_id
        self.conversion_rate = conversion_rate
        self.is_base_unit = is_base_unit