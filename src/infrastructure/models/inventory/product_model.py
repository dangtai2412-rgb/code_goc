from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from infrastructure.databases.base import Base

class ProductModel(Base):
    __tablename__ = 'products'
    #__table_args__ = {'extend_existing': True}

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    selling_price = Column(Numeric(12, 2))
    stock_quantity = Column(Integer)
    
    # Khóa ngoại: Sản phẩm thuộc sở hữu của ai
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))