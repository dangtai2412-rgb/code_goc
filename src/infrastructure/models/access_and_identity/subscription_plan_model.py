from sqlalchemy import Column, Integer, String, Numeric
from infrastructure.databases.base import Base

class SubscriptionPlanModel(Base):
    __tablename__ = 'subscription_plans'
    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_name = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False) # Số ngày hiệu lực
    price = Column(Numeric(12, 2), nullable=False)
    description = Column(String(255), nullable=True) # Mô tả gói