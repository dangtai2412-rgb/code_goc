class Payment:
    def __init__(self, debt_id, amount_paid, payment_method, payment_date=None, payment_id=None):
        self.payment_id = payment_id
        self.debt_id = debt_id
        self.amount_paid = amount_paid
        self.payment_method = payment_method
        self.payment_date = payment_date