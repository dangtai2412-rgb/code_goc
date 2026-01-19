from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.databases.base import Base

class ReturnOrderDetailModel(Base):
    __tablename__ = 'return_order_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    return_id = Column(Integer, ForeignKey('return_orders.return_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    condition = Column(String(50), default='Good')