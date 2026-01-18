from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class OrderModel(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    employee_id = Column(Integer, ForeignKey('employees.employee_id')) # Người tạo đơn
    order_date = Column(Date)
    order_status = Column(String(20), default="Pending") # Pending, Completed, Cancelled
    payment_method = Column(String(50))
    total_amount = Column(Numeric(12, 2), default=0)

    # Quan hệ 1-nhiều với chi tiết đơn hàng
    details = relationship("OrderDetailModel", back_populates="order", cascade="all, delete-orphan")