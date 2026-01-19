# src/infrastructure/models/access_and_identity/business_owner_model.py
from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.databases.base import Base

class BusinessOwnerModel(Base):
    __tablename__ = 'business_owners'
    owner_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15), nullable=True)
    account_status = Column(String(20), default='Active')
    
    # Khóa ngoại trỏ sang bảng gói cước
    plan_id = Column(Integer, ForeignKey('subscription_plans.plan_id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('administrators.admin_id'), nullable=True)