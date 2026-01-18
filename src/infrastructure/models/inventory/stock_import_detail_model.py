from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
import datetime


class StockImportDetailModel(Base):
    __tablename__ = 'stock_import_details'
    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    import_id = Column(Integer, ForeignKey('stock_imports.import_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(18, 2), nullable=False)