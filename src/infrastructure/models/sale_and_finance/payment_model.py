from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class PaymentModel(Base):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    debt_id = Column(Integer, ForeignKey('debts.debt_id'), nullable=False)
    
    amount_paid = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    payment_method = Column(String(50)) # Tiền mặt, Chuyển khoản