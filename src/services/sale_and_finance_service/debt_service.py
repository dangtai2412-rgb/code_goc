class DebtService:
    def __init__(self, repository):
        self.repository = repository

    def create_debt_from_order(self, order_id, customer_id, amount):
        # Logic: Có thể kiểm tra hạn mức nợ của khách trước khi cho nợ
        return self.repository.add(order_id, customer_id, amount)

    def get_customer_debts(self, customer_id):
        return self.repository.get_by_customer(customer_id)