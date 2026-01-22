class DebtService:
    def __init__(self, repository):
        self.repository = repository

    def create_debt_from_order(self, order_id, customer_id, owner_id, amount):
        # Gọi xuống Repository để lưu vào Database
        return self.repository.add(
            order_id=order_id, 
            customer_id=customer_id, 
            owner_id=owner_id, 
            amount=amount
        )

    