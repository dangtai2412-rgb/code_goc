from infrastructure.models.sale_and_finance.expense_model import ExpenseModel

class ExpenseRepository:
    def __init__(self, session):
        self.session = session

    def add(self, expense_model):
        self.session.add(expense_model)
        self.session.commit()
        return expense_model

    def get_by_owner(self, owner_id):
        return self.session.query(ExpenseModel).filter_by(owner_id=owner_id).order_by(ExpenseModel.expense_date.desc()).all()