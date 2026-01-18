class Debt:
    def __init__(self, order_id, customer_id, debt_amount, debt_status="Unpaid", debt_created_date=None, debt_id=None):
        self.debt_id = debt_id
        self.order_id = order_id
        self.customer_id = customer_id
        self.debt_amount = debt_amount
        self.debt_status = debt_status
        self.debt_created_date = debt_created_date