class DebtService:
    def __init__(self, repository):
        self.repository = repository

    def create_debt_from_order(self, order_id, customer_id, amount):
       
        return self.repository.add(order_id, customer_id, amount)

    def create_debt_from_order(self, order_id, customer_id, owner_id, amount):
       
        return self.repository.add(order_id, customer_id, owner_id, amount)