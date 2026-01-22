from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.databases.base import Base

class InventoryCheckDetailModel(Base):
    __tablename__ = 'inventory_check_details'

    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    check_id = Column(Integer, ForeignKey('inventory_checks.check_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    
    system_quantity = Column(Integer, nullable=False) # Tồn kho trước khi kiểm
    actual_quantity = Column(Integer, nullable=False) # Tồn kho thực tế đếm được
    variance = Column(Integer, nullable=False)        # Chênh lệch (Thực tế - Hệ thống)
    reason = Column(String(255), nullable=True)       # Lý do (Vỡ, mất, nhầm lẫn...)
    