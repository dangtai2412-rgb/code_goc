from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel
from domain.models.order_detail import OrderDetail
from infrastructure.databases.mssql import session

class OrderDetailRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, detail: OrderDetail):
        try:
            db_detail = OrderDetailModel(
                order_id=detail.order_id,
                product_id=detail.product_id,
                unit_id=detail.unit_id,
                order_quantity=detail.order_quantity,
                unit_price=detail.unit_price,
                line_total=detail.line_total
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