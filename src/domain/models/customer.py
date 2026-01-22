class Customer:
    def __init__(self, customer_name, owner_id, phone_number=None, address=None, email=None, customer_id=None):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.owner_id = owner_id
        self.phone_number = phone_number
        self.address = address
        self.email = email