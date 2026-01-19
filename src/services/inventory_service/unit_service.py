from domain.models.unit import Unit

class UnitService:
    def __init__(self, unit_repo):
        self.unit_repo = unit_repo

    def add_unit(self, data):
        product_id = data.get('product_id')
        is_base = data.get('is_base_unit', False)

        # LOGIC: Nếu đây là đơn vị cơ bản, kiểm tra xem sản phẩm đã có đơn vị cơ bản chưa
        if is_base:
            existing_units = self.unit_repo.get_by_product(product_id)
            for u in existing_units:
                if u.is_base_unit:
                    raise Exception("Sản phẩm này đã có đơn vị tính cơ bản rồi!")

        new_unit = Unit(
            product_id=product_id,
            unit_name=data.get('unit_name'),
            conversion_rate=data.get('conversion_rate', 1),
            is_base_unit=is_base
        )
        return self.unit_repo.add(new_unit)

    # BỔ SUNG: Hàm lấy danh sách đơn vị theo sản phẩm
    def get_units_by_product(self, product_id):
        return self.unit_repo.get_by_product(product_id)
    def delete_unit(self, unit_id):
        return self.unit_repo.delete(unit_id)