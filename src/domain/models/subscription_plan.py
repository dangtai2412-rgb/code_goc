class SubscriptionPlan:
    def __init__(self, plan_name, duration, price, plan_id=None):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.duration = duration
        self.price = price