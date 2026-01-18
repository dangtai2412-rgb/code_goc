from infrastructure.models.sale_and_finance.debt_model import DebtModel
from domain.models.debt import Debt
from infrastructure.databases.mssql import session

class DebtRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, debt: Debt):
        try:
            db_debt = DebtModel(
                order_id=debt.order_id,
                customer_id=debt.customer_id,
                debt_amount=debt.debt_amount,
                debt_status=debt.debt_status,
                debt_created_date=debt.debt_created_date
            )
            self.session.add(db_debt)
            self.session.commit()
            self.session.refresh(db_debt)
            return db_debt
        except Exception as e:
            self.session.rollback()
            raise e
    def get_by_customer(self, customer_id):
        return self.session.query(DebtModel).filter_by(customer_id=customer_id).all()