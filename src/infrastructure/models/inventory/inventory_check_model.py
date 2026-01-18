from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class InventoryCheckModel(Base):
    __tablename__ = 'inventory_checks'

    check_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    
    check_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default='Completed') # Completed: Đã cân bằng kho
    note = Column(String(255), nullable=True)

    # Relationship
    details = relationship("InventoryCheckDetailModel", backref="inventory_check", cascade="all, delete-orphan")