from infrastructure.models.sale_and_finance.debt_model import DebtModel
from domain.models.debt import Debt
from infrastructure.databases.mssql import session

class DebtRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, order_id, customer_id, debt_amount, debt_status='Unpaid'): # Nhận đủ tham số
        try:
            db_debt = DebtModel(
                order_id=order_id,
                customer_id=customer_id,
                debt_amount=debt_amount,
                debt_status=debt_status
            )
            self.db_session.add(db_debt)
            self.db_session.commit()
            self.db_session.refresh(db_debt)
            return db_debt
        except Exception as e:
            self.db_session.rollback()
            raise e
    def get_by_customer(self, customer_id):
        return self.session.query(DebtModel).filter_by(customer_id=customer_id).all()