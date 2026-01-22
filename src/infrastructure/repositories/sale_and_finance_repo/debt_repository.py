from infrastructure.models.sale_and_finance.debt_model import DebtModel
from domain.models.debt import Debt
from infrastructure.databases.mssql import session

class DebtRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, order_id, customer_id, owner_id, amount, debt_status='Active'):
        try:
            db_debt = DebtModel(
                order_id=order_id,
                customer_id=customer_id,
                owner_id=owner_id,        
                total_debt=amount,        
                remaining_debt=amount,
                debt_status=debt_status
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
    def get_by_id(self, debt_id, owner_id):
        # Lấy khoản nợ theo ID và phải đúng chủ cửa hàng
        return self.session.query(DebtModel).filter_by(
            debt_id=debt_id, 
            owner_id=owner_id
        ).first()