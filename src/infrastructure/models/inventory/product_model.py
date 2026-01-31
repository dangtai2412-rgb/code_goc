from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship 
from infrastructure.databases.base import Base

class ProductModel(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    sku = Column(String(50), unique=True)
    
    # Giá vốn và giá bán
    cost_price = Column(Numeric(12, 2), default=0) 
    selling_price = Column(Numeric(12, 2), nullable=False)
    stock_quantity = Column(Integer, default=0)
    
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=True)
    unit_id = Column(Integer, ForeignKey('units.unit_id'), nullable=True)

    # --- PHẦN SỬA LỖI Ở ĐÂY ---
    
    # 1. Liên kết với bảng Category (giữ nguyên)
    category = relationship("CategoryModel", lazy="joined")
    
    # 2. Liên kết với bảng Unit (THÊM foreign_keys=[unit_id])
    # Dòng này giúp SQLAlchemy biết chính xác phải dùng cột unit_id để nối bảng
    unit = relationship("UnitModel", foreign_keys=[unit_id], lazy="joined")