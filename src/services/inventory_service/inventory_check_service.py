from infrastructure.models.inventory.inventory_check_model import InventoryCheckModel
from infrastructure.models.inventory.inventory_check_detail_model import InventoryCheckDetailModel

class InventoryCheckService:
    def __init__(self, check_repo, product_repo):
        self.check_repo = check_repo
        self.product_repo = product_repo

    def perform_inventory_check(self, owner_id, data):
        """
        Logic cân bằng kho:
        1. Tạo phiếu kiểm kho
        2. Với mỗi sản phẩm: Lưu chi tiết & Cập nhật lại stock_quantity thực tế
        3. Commit một lần duy nhất
        """
        try:
            # 1. Tạo Header phiếu kiểm
            new_check = InventoryCheckModel(
                owner_id=owner_id,
                check_date=data.get('check_date'),
                notes=data.get('notes')
            )
            self.check_repo.add(new_check)

            # 2. Xử lý từng sản phẩm trong danh sách kiểm
            for item in data.get('details', []):
                product_id = item['product_id']
                actual_qty = item['actual_quantity'] # Số lượng thực tế đếm được

                # Lưu chi tiết phiếu kiểm
                detail = InventoryCheckDetailModel(
                    check_id=new_check.check_id,
                    product_id=product_id,
                    expected_quantity=item['expected_quantity'], # Số lượng trên máy
                    actual_quantity=actual_qty
                )
                # Giả sử bạn có detail_repo hoặc lưu trực tiếp qua session
                self.check_repo.session.add(detail)

                # CẬP NHẬT KHO: Đưa tồn kho thực tế về đúng số lượng đếm được
                product = self.product_repo.get_by_id(product_id)
                if product:
                    product.stock_quantity = actual_qty
            
            # 3. CHỐT GIAO DỊCH: Lưu tất cả thay đổi
            self.check_repo.commit()
            return new_check

        except Exception as e:
            self.check_repo.session.rollback()
            raise e