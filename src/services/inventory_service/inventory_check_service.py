from datetime import datetime
from infrastructure.models.inventory.inventory_check_model import InventoryCheckModel
from infrastructure.models.inventory.inventory_check_detail_model import InventoryCheckDetailModel

class InventoryCheckService:
    # 👇 Inject product_repository để update lại kho
    def __init__(self, repository, product_repository):
        self.repo = repository
        self.product_repo = product_repository

    def create_check(self, data, owner_id):
        # 1. Tạo phiếu kiểm header
        new_check = InventoryCheckModel(
            owner_id=owner_id,
            note=data.get('note', ''),
            check_date=datetime.now(),
            status='Completed' 
        )
        self.repo.session.add(new_check)
        self.repo.session.flush() # Lấy ID

        # 2. Xử lý chi tiết & CẬP NHẬT KHO
        items = data.get('details', [])
        for item in items:
            product_id = item['product_id']
            actual_qty = int(item['actual_quantity'])

            # Lấy sản phẩm hiện tại để xem tồn kho hệ thống
            product = self.product_repo.get_by_id(product_id)
            if not product:
                continue # Bỏ qua nếu ID sai

            system_qty = product.stock_quantity
            variance = actual_qty - system_qty

            # Tạo detail
            detail = InventoryCheckDetailModel(
                check_id=new_check.check_id,
                product_id=product_id,
                system_quantity=system_qty,
                actual_quantity=actual_qty,
                variance=variance,
                reason=item.get('reason', '')
            )
            self.repo.session.add(detail)

            # 🔥 UPDATE LẠI KHO THEO SỐ THỰC TẾ
            product.stock_quantity = actual_qty
            # (Product đã được attach vào session nên không cần gọi repo.update explicit, commit là tự lưu)

        # 3. Lưu tất cả thay đổi
        self.repo.commit()
        return new_check

    def get_history(self, owner_id):
        return self.repo.get_all(owner_id)

    def get_detail(self, check_id):
        return self.repo.get_by_id(check_id)