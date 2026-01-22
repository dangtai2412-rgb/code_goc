# src/infrastructure/models/sale_and_finance/payment_model.py

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from infrastructure.databases.base import Base
from datetime import datetime
from infrastructure.models.access_and_identity.business_owner_model import BusinessOwnerModel

class PaymentModel(Base):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # SỬA: Phải là business_owners.owner_id
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False) 
    
    # Các cột này phải có trong DB
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=True)
    debt_id = Column(Integer, ForeignKey('debts.debt_id'), nullable=True)
    
    amount = Column(Numeric(18, 2), nullable=False)
    payment_method = Column(String(50))
    payment_date = Column(DateTime, default=datetime.utcnow)
    note = Column(String(255))