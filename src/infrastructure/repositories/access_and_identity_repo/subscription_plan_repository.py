from infrastructure.models.access_and_identity.subscription_plan_model import SubscriptionPlanModel
from infrastructure.databases.mssql import session

class SubscriptionPlanRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, name, duration, price):
        db_plan = SubscriptionPlanModel(
            plan_name=name, 
            duration=duration, 
            price=price
        )
        self.session.add(db_plan)
        self.session.commit()
        self.session.refresh(db_plan)
        return db_plan

    def get_all(self):
        return self.session.query(SubscriptionPlanModel).all()