class Expense:
    def __init__(self, description, amount, expense_date, owner_id, expense_id=None):
        self.expense_id = expense_id
        self.description = description
        self.amount = amount
        self.expense_date = expense_date
        self.owner_id = owner_id