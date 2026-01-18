class BusinessOwner:
    def __init__(self, owner_name, admin_id, plan_id, phone_number=None, email=None, account_status=None, owner_id=None):
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.admin_id = admin_id   # Khóa ngoại nối đến Admin
        self.plan_id = plan_id     # Khóa ngoại nối đến SubscriptionPlan
        self.phone_number = phone_number
        self.email = email
        self.account_status = account_status