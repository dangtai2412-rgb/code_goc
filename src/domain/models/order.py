class Order:
    def __init__(self, customer_id, employee_id, order_date, total_amount=0, order_status="Pending", payment_method="Cash", order_id=None):
        self.order_id = order_id
        self.customer_id = customer_id # Khóa ngoại
        self.employee_id = employee_id # Khóa ngoại
        self.order_date = order_date
        self.order_status = order_status
        self.payment_method = payment_method
        self.total_amount = total_amount