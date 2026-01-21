from infrastructure.models.sale_and_finance.expense_model import ExpenseModel
from domain.models.expense import Expense

class ExpenseRepository:
    def __init__(self, db_session):
        self.session = db_session

    def add(self, exp: Expense): # SỬA: Nhận Domain Object
        db_expense = ExpenseModel(
            description=exp.description,
            amount=exp.amount,
            expense_date=exp.expense_date,
            owner_id=exp.owner_id
        )
        try:
            self.session.add(db_expense)
            self.session.commit()
            return db_expense
        except Exception as e:
            self.session.rollback()
            raise e