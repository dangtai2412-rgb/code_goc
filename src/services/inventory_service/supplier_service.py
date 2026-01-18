from infrastructure.models.inventory.supplier_model import SupplierModel

class SupplierService:
    def __init__(self, repository):
        self.repository = repository

    def create_supplier(self, data, owner_id):
        new_supplier = SupplierModel(
            owner_id=owner_id,
            supplier_name=data['supplier_name'],
            phone_number=data.get('phone_number'),
            tax_code=data.get('tax_code')
        )
        return self.repository.add(new_supplier)

    def get_suppliers(self, owner_id):
        return self.repository.get_all_by_owner(owner_id)

    def update_supplier(self, supplier_id, owner_id, data):
        supplier = self.repository.get_by_id(supplier_id, owner_id)
        if not supplier:
            return None
        
        supplier.supplier_name = data.get('supplier_name', supplier.supplier_name)
        supplier.phone_number = data.get('phone_number', supplier.phone_number)
        supplier.tax_code = data.get('tax_code', supplier.tax_code)
        
        self.repository.update()
        return supplier