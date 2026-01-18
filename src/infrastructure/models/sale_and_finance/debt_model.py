from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from infrastructure.databases.base import Base
class DebtModel(Base):
    __tablename__ = 'debts'
    #__table_args__ = {'extend_existing': True}
    debt_id = Column(Integer, primary_key=True, autoincrement=True)
    debt_amount = Column(Numeric(12, 2))
    debt_created_date = Column(Date)
    debt_status = Column(String(20))
    # Khóa ngoại
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))