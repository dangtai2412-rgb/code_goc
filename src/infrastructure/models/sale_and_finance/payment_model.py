from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from infrastructure.databases.base import Base

class PaymentModel(Base):
    __tablename__ = 'payments'
    #__table_args__ = {'extend_existing': True}

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    amount_paid = Column(Numeric(12, 2))
    payment_date = Column(Date)
    payment_method = Column(String(50))
    
    # Khóa ngoại: Thanh toán này cho khoản nợ nào
    debt_id = Column(Integer, ForeignKey('debts.debt_id'))