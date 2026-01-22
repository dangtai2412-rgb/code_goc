from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel
from domain.models.order_detail import OrderDetail
from infrastructure.databases.mssql import session

class OrderDetailRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, data):
        try:
            db_detail = OrderDetailModel(
                # SỬA: Thay . thành .get() vì data là dictionary
                order_id=data.get('order_id'),
                product_id=data.get('product_id'),
                quantity=data.get('quantity', 0),
                unit_price=data.get('unit_price', 0),
                # Tự tính thành tiền nếu chưa có
                line_total=data.get('quantity', 0) * data.get('unit_price', 0)
            )
            self.session.add(db_detail)
            self.session.commit()
            self.session.refresh(db_detail)
            return db_detail
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_order(self, order_id):
        return self.session.query(OrderDetailModel).filter_by(order_id=order_id).all()