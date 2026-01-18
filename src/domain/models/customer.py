class Customer:
    def __init__(self, customer_name, owner_id, phone_number=None, address=None, total_outstanding_debt=0, customer_id=None):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.owner_id = owner_id # Khóa ngoại nối đến BusinessOwner
        self.phone_number = phone_number
        self.address = address
        self.total_outstanding_debt = total_outstanding_debt