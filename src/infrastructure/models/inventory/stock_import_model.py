from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
import datetime


class StockImportModel(Base):
    __tablename__ = 'stock_imports'
    import_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'))
    import_date = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Numeric(18, 2), default=0) # Chuẩn cho báo cáo kế toán

