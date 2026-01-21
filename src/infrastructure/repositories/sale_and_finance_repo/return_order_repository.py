from infrastructure.models.sale_and_finance.return_order_model import ReturnOrderModel

class ReturnOrderRepository:
    def __init__(self, db_session):
        self.session = db_session

    # Lưu phiếu trả nhưng chưa commit (để Service xử lý kho xong mới commit 1 thể)
    def add_pending(self, return_order):
        self.session.add(return_order)
        self.session.flush() # Để lấy ID nhưng chưa chốt DB
        return return_order

    def commit(self):
        self.session.commit()