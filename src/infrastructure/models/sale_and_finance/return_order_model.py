from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class ReturnOrderModel(Base):
    __tablename__ = 'return_orders'

    return_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    
    return_date = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String(255), nullable=True) # Lý do trả: Hàng lỗi, Khách đổi ý...
    refund_amount = Column(Numeric(12, 2), default=0) # Số tiền hoàn lại cho khách
    
    # Quan hệ với bảng chi tiết trả hàng
    return_details = relationship("ReturnOrderDetailModel", backref="return_order")