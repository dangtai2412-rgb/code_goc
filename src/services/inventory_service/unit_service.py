from domain.models.unit import Unit

class UnitService:
    def __init__(self, unit_repo):
        self.unit_repo = unit_repo

    def create_unit(self, data, owner_id):
        new_unit = Unit(
            unit_name=data.get('unit_name'),
            description=data.get('description'),
            owner_id=owner_id # Đảm bảo có owner_id
        )
        return self.unit_repo.add(new_unit)

    # BỔ SUNG: Hàm lấy danh sách đơn vị theo sản phẩm
    def get_units_by_product(self, product_id):
        return self.unit_repo.get_by_product(product_id)
    def delete_unit(self, unit_id):
        return self.unit_repo.delete(unit_id)
    # src/services/inventory_service/unit_service.py
    def get_units_by_product(self, product_id):
        """Nghiệp vụ lấy đơn vị tính theo sản phẩm"""
        return self.unit_repo.get_by_product(product_id)
    def get_units(self, owner_id):
        return self.unit_repo.get_all_by_owner(owner_id)