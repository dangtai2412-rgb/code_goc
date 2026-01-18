from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from infrastructure.databases.base import Base

class UnitModel(Base):
    __tablename__ = 'units'
    #__table_args__ = {'extend_existing': True}

    unit_id = Column(Integer, primary_key=True, autoincrement=True)
    unit_name = Column(String(100), nullable=False)
    conversion_rate = Column(Numeric(10, 4))
    is_base_unit = Column(Boolean, default=True)
    
    # Khóa ngoại: Đơn vị này dùng cho sản phẩm nào
    product_id = Column(Integer, ForeignKey('products.product_id'))