from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class OrderDetailModel(Base):
    __tablename__ = 'order_details'
    
    # Khóa chính phức hợp (Composite Key) theo ERD
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    unit_id = Column(Integer, ForeignKey('units.unit_id'), primary_key=True)

    order_quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False) # Giá tại thời điểm bán
    line_total = Column(Numeric(12, 2), nullable=False) # = quantity * price

    order = relationship("OrderModel", back_populates="details")