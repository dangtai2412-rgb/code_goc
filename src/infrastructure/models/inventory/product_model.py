from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from infrastructure.databases.base import Base

class ProductModel(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    sku = Column(String(50), unique=True)
    
    # QUAN TRỌNG: Cần giá vốn để tính lợi nhuận
    cost_price = Column(Numeric(12, 2), default=0) 
    selling_price = Column(Numeric(12, 2), nullable=False)
    stock_quantity = Column(Integer, default=0)
    
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=True)
    # unit_id ở đây đại diện cho đơn vị tính cơ bản (Vd: Cái, Thùng)
    unit_id = Column(Integer, ForeignKey('units.unit_id'), nullable=True)