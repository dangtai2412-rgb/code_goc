# src/infrastructure/repositories/sale_and_finance_repo/order_repository.py
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models.sale_and_finance.order_model import OrderModel

class OrderRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(OrderModel, db_session)

    def get_orders_by_owner(self, owner_id):
        return self.model.query.filter_by(owner_id=owner_id).order_by(self.model.created_at.desc()).all()

    # --- THÊM HÀM NÀY ---
    def get_all_pagination(self, owner_id, limit, offset):
        """Lấy danh sách đơn hàng có phân trang"""
        query = self.session.query(self.model).filter_by(owner_id=owner_id)
        
        # Đếm tổng số bản ghi để Frontend biết có bao nhiêu trang
        total = query.count()
        
        # Lấy dữ liệu trang hiện tại
        items = query.order_by(self.model.order_id.desc()).limit(limit).offset(offset).all()
        
        return items, total
    