from infrastructure.models.inventory.supplier_model import SupplierModel
from domain.models.supplier import Supplier
class SupplierService:
    def __init__(self, repository):
        self.repository = repository

    def create_supplier(self, data, owner_id):
        # Đóng gói vào đối tượng Domain
        new_supplier = Supplier(
            supplier_name=data.get('supplier_name'),
            owner_id=owner_id,
            phone_number=data.get('phone_number'),
            tax_code=data.get('tax_code')
        )
        return self.repository.add(new_supplier)

    def get_suppliers_by_owner(self, owner_id):
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