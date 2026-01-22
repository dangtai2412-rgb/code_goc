from infrastructure.models.sale_and_finance.debt_model import DebtModel
from infrastructure.models.sale_and_finance.payment_model import PaymentModel
from domain.models.payment import Payment
from infrastructure.databases.mssql import session
import datetime
class PaymentRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, data, owner_id):
        try:
            new_payment = PaymentModel(
                owner_id=owner_id,
                order_id=data.get('order_id'),
                customer_id=data.get('customer_id'),
                debt_id=data.get('debt_id'), # Bổ sung để lưu vết thanh toán nợ
                amount=data.get('amount'),
                payment_method=data.get('payment_method', 'Cash'),
                payment_date=datetime.datetime.now(), # Sửa: datetime.datetime.now()
                note=data.get('note')
            )
            self.session.add(new_payment)
            self.session.commit()
            self.session.refresh(new_payment)
            
            return new_payment  # QUAN TRỌNG: Phải có dòng này!
        except Exception as e:
            self.session.rollback()
            raise e
        