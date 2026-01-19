from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class DebtModel(Base):
    __tablename__ = 'debts'

    debt_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=True)
    
    total_debt = Column(Numeric(12, 2), nullable=False)
    remaining_debt = Column(Numeric(12, 2), nullable=False) # Số nợ còn lại sau khi trả một phần
    debt_created_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=True)
    # Active, Paid, Overdue
    debt_status = Column(String(20), default='Active')