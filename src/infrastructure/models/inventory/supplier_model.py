from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
import datetime


class SupplierModel(Base):
    __tablename__ = 'suppliers'
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))
    supplier_name = Column(String(100), nullable=False) # Dùng String cho MSSQL
    phone_number = Column(String(20))
    tax_code = Column(String(50))