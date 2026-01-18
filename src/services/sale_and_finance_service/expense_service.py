from datetime import datetime
from infrastructure.models.sale_and_finance.expense_model import ExpenseModel

class ExpenseService:
    def __init__(self, repository):
        self.repo = repository

    def create_expense(self, data, owner_id):
        amount = data.get('amount')
        if not amount or float(amount) <= 0:
            raise ValueError("Số tiền chi phải lớn hơn 0")

        new_expense = ExpenseModel(
            owner_id=owner_id,
            expense_category=data.get('category', 'Chi phí khác'),
            amount=float(amount),
            description=data.get('description', ''),
            expense_date=datetime.now()
        )
        return self.repo.add(new_expense)

    def get_history(self, owner_id):
        return self.repo.get_by_owner(owner_id)