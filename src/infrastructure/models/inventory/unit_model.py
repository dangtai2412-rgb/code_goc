from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from infrastructure.databases.base import Base

class UnitModel(Base):
    __tablename__ = 'units'

    unit_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False) # Thêm owner_id
    unit_name = Column(String(100), nullable=False)
    conversion_rate = Column(Numeric(10, 4), default=1)
    is_base_unit = Column(Boolean, default=True)
    description = Column(String(255), nullable=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=True)