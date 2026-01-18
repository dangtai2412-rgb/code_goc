from infrastructure.models.sale_and_finance.payment_model import PaymentModel
from domain.models.payment import Payment
from infrastructure.databases.mssql import session

class PaymentRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, p: Payment):
        try:
            db_payment = PaymentModel(
                debt_id=p.debt_id,
                amount_paid=p.amount_paid,
                payment_method=p.payment_method,
                payment_date=p.payment_date
            )
            self.session.add(db_payment)
            self.session.commit()
            self.session.refresh(db_payment)
            return db_payment
        except Exception as e:
            self.session.rollback()
            raise e