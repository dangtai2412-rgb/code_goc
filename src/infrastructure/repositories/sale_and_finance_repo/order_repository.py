from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.inventory.product_model import ProductModel
from infrastructure.databases.mssql import session
class OrderRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, order_model):
        """Chỉ thực hiện lưu, không chứa logic trừ kho"""
        try:
            self.session.add(order_model)
            # Không commit ở đây để Service quản lý Transaction
            return order_model
        except Exception as e:
            self.session.rollback()
            raise e
    def get_all_by_owner(self, owner_id):
        # Lấy toàn bộ đơn hàng của chủ shop, sắp xếp theo ngày mới nhất
        return self.session.query(OrderModel).filter_by(owner_id=owner_id).order_by(OrderModel.order_date.desc()).all()