class Customer:
    def __init__(self, customer_name, phone_number=None, address=None, owner_id=None, customer_id=None):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.address = address
        self.owner_id = owner_id