from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class OrderModel(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=True)
    # Người tạo đơn (có thể là chủ hoặc nhân viên)
    created_by = Column(Integer, nullable=True) 
    
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    # UNPAID, PAID, PARTIAL
    payment_status = Column(String(20), default='UNPAID') 
    payment_method = Column(String(50)) # Cash, Transfer, Debt
    total_amount = Column(Numeric(12, 2), nullable=False)

    # Quan hệ với chi tiết đơn hàng
    details = relationship("OrderDetailModel", backref="order", cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "order_id": self.order_id,
            "owner_id": self.owner_id,
            "customer_id": self.customer_id,
            "total_amount": float(self.total_amount) if self.total_amount else 0,
            "payment_status": self.payment_status,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "payment_method": self.payment_method
        }