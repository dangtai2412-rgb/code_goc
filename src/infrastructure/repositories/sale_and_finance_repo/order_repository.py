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