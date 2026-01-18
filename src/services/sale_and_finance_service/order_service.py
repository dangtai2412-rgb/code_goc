from datetime import datetime
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel
from infrastructure.models.sale_and_finance.debt_model import DebtModel

class OrderService:
    # Inject thêm product_repo và debt_service
    def __init__(self, repository, product_repo, debt_service):
        self.repo = repository
        self.product_repo = product_repo
        self.debt_service = debt_service

    def create_order(self, data, user_id):
        # 1. Tạo đơn hàng chính
        new_order = OrderModel(
            owner_id=data.get('owner_id'), # Hoặc lấy từ user_id nếu cần logic
            customer_id=data.get('customer_id'),
            total_amount=data.get('total_amount'),
            payment_status=data.get('payment_status', 'UNPAID'),
            payment_method=data.get('payment_method'),
            created_by=user_id
        )
        saved_order = self.repo.add(new_order)

        # 2. Xử lý chi tiết đơn hàng & TRỪ KHO (Real-time Inventory)
        details = data.get('details', [])
        for item in details:
            # Lưu chi tiết
            detail_model = OrderDetailModel(
                order_id=saved_order.order_id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            )
            self.repo.session.add(detail_model)

            # --- TRỪ KHO ---
            product = self.product_repo.get_by_id(item['product_id'])
            if product:
                if product.stock_quantity < item['quantity']:
                    raise ValueError(f"Sản phẩm {product.product_name} không đủ tồn kho!")
                product.stock_quantity -= item['quantity']
        
        # 3. Xử lý CÔNG NỢ (Debt Management)
        # Nếu khách chưa trả đủ tiền -> Ghi nợ tự động
        paid_amount = data.get('paid_amount', 0)
        total = data.get('total_amount', 0)
        
        if paid_amount < total and saved_order.customer_id:
            debt_amount = total - paid_amount
            # Gọi Debt Service để ghi nhận
            # (Lưu ý: Bạn cần đảm bảo DebtService có hàm add_debt)
            new_debt = DebtModel(
                customer_id=saved_order.customer_id,
                order_id=saved_order.order_id,
                total_debt=debt_amount,
                remaining_debt=debt_amount,
                due_date=datetime.now() # Hoặc + 30 ngày
            )
            self.repo.session.add(new_debt)

        self.repo.session.commit()
        return saved_order
    
    def get_all_orders(self, owner_id):
        return self.repo.get_by_owner(owner_id)