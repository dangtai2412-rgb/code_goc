from sqlalchemy import Column, Integer, Numeric, ForeignKey
from infrastructure.databases.base import Base

class OrderDetailModel(Base):
    __tablename__ = 'order_details'

    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    # Thành tiền = quantity * unit_price
    line_total = Column(Numeric(12, 2), nullable=False)