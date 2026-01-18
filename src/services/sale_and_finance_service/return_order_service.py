from datetime import datetime
from infrastructure.models.sale_and_finance.return_order_model import ReturnOrderModel
from infrastructure.models.sale_and_finance.return_order_detail_model import ReturnOrderDetailModel

class ReturnOrderService:
    # Inject ProductRepo để update tồn kho
    def __init__(self, repository, product_repo):
        self.repo = repository
        self.product_repo = product_repo

    def create_return(self, data, owner_id):
        # 1. Tạo phiếu trả
        order_id = data.get('order_id')
        new_return = ReturnOrderModel(
            owner_id=owner_id,
            order_id=order_id,
            reason=data.get('reason'),
            refund_amount=data.get('refund_amount', 0),
            return_date=datetime.now()
        )
        saved_return = self.repo.add_pending(new_return)

        # 2. Xử lý từng món hàng trả
        items = data.get('details', [])
        for item in items:
            product_id = item['product_id']
            qty = int(item['quantity'])

            # Lưu chi tiết trả
            detail = ReturnOrderDetailModel(
                return_id=saved_return.return_id,
                product_id=product_id,
                quantity=qty,
                condition=item.get('condition', 'Good')
            )
            self.repo.session.add(detail)

            # 3. CỘNG LẠI KHO (Nếu hàng còn tốt)
            # Nếu condition là 'Broken' (hỏng) thì có thể chọn không cộng kho
            if item.get('condition', 'Good') == 'Good':
                product = self.product_repo.get_by_id(product_id)
                if product:
                    product.stock_quantity += qty
        
        # 4. Chốt giao dịch
        self.repo.commit()
        return saved_return