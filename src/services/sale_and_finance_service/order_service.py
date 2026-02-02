from infrastructure.repositories.sale_and_finance_repo.order_repository import OrderRepository
from infrastructure.repositories.sale_and_finance_repo.order_detail_repository import OrderDetailRepository
# Import các model cần thiết...
from error_handler import CustomError
from domain.models.order import Order # Giả sử bạn có model này
from flask_sqlalchemy import SQLAlchemy # Cần db session để quản lý transaction

class OrderService:
    def __init__(self, order_repo: OrderRepository, order_detail_repo: OrderDetailRepository, db):
        self.order_repo = order_repo
        self.order_detail_repo = order_detail_repo
        self.db = db # Cần inject db instance vào đây

    def create_order(self, data, owner_id, created_by_id):
        # Bắt đầu Transaction
        try:
            # 1. Tạo Order Header
            details_data = data.pop('details') # Tách phần chi tiết ra
            
            new_order = self.order_repo.create(
                owner_id=owner_id,
                customer_id=data['customer_id'],
                total_amount=data['total_amount'],
                # ... mapping các trường khác từ data ...
            )
            self.db.session.flush() # Đẩy ID mới sinh ra nhưng chưa commit

            # 2. Tạo Order Details
            for item in details_data:
                self.order_detail_repo.create(
                    order_id=new_order.order_id, # Lấy ID vừa flush
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price']
                )
                # Tùy chọn: Trừ kho (Stock) tại đây luôn
            
            self.db.session.commit() # Nếu mọi thứ ổn thì Lưu thật
            return new_order

        except Exception as e:
            self.db.session.rollback() # CÓ LỖI LÀ HOÀN TÁC TOÀN BỘ
            raise CustomError(f"Lỗi tạo đơn hàng: {str(e)}", 400)

    def get_orders_by_owner(self, owner_id, page=1, limit=20):
        # Logic phân trang nên nằm ở Repository, nhưng gọi tạm ở đây
        offset = (page - 1) * limit
        return self.order_repo.get_all_pagination(owner_id, limit, offset)