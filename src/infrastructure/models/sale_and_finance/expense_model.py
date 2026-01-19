from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class ExpenseModel(Base):
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    
    expense_category = Column(String(100), nullable=False) # VD: Tiền điện, Nhập hàng, Lương
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String(255), nullable=True)
    expense_date = Column(DateTime(timezone=True), server_default=func.now())