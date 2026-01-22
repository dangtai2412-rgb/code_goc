class Supplier:
    def __init__(self, supplier_name, owner_id, phone_number=None, tax_code=None, supplier_id=None):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.owner_id = owner_id
        self.phone_number = phone_number
        self.tax_code = tax_code