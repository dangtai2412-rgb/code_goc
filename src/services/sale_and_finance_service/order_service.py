from datetime import datetime
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel

class OrderService:
    def __init__(self, repository, product_repo, debt_service):
        self.repo = repository
        self.product_repo = product_repo
        self.debt_service = debt_service

    def create_order(self, data, user_id):
        try:
            # 1. Tạo đơn hàng chính
            new_order = OrderModel(
                owner_id=data.get('owner_id'),
                customer_id=data.get('customer_id'),
                total_amount=data.get('total_amount', 0),
                payment_status=data.get('payment_status', 'UNPAID'),
                payment_method=data.get('payment_method'),
                created_by=user_id,
                order_date=datetime.now()
            )
            # Chỉ add vào session, chưa commit
            self.repo.add(new_order)
            self.repo.session.flush()
            # 2. Xử lý chi tiết đơn hàng & TRỪ KHO
            details = data.get('details', [])
            for item in details:
                # Lưu chi tiết
                detail_model = OrderDetailModel(
                    order_id=new_order.order_id, # SQLAlchemy sẽ tự lấy ID sau khi flush/commit
                    product_id=item['product_id'],
                    order_quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    line_total=item['quantity'] * item['unit_price']
                )
                self.repo.session.add(detail_model)

                # --- TRỪ KHO ---
                product = self.product_repo.get_by_id(item['product_id'])
                if not product:
                    raise ValueError(f"Sản phẩm ID {item['product_id']} không tồn tại")
                
                if product.stock_quantity < item['quantity']:
                    raise ValueError(f"Sản phẩm {product.product_name} không đủ tồn kho!")
                
                product.stock_quantity -= item['quantity']
        
            # 3. Xử lý CÔNG NỢ (Debt Management)
            paid_amount = float(data.get('paid_amount', 0))
            total = float(data.get('total_amount', 0))
            
            if paid_amount < total and new_order.customer_id:
                debt_amount = total - paid_amount
                # Ghi nợ thông qua DebtService (Để logic xử lý nợ nằm riêng bên đó)
                self.debt_service.create_debt_from_order(
                    customer_id=new_order.customer_id,
                    order_id=new_order.order_id,
                    amount=debt_amount
                )

            # 4. CHỐT GIAO DỊCH: Nếu mọi thứ ok thì lưu tất cả cùng lúc
            self.repo.session.commit()
            return new_order

        except Exception as e:
            # Nếu có bất kỳ lỗi nào xảy ra, hủy bỏ toàn bộ các thao tác trên
            self.repo.session.rollback()
            raise e