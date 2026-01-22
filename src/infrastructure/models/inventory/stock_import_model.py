from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class StockImportModel(Base):
    __tablename__ = 'stock_imports'
    import_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=False)
    
    import_date = Column(DateTime(timezone=True), server_default=func.now())
    total_amount = Column(Numeric(18, 2), default=0)
    
    # Thêm thông tin thanh toán để quản lý công nợ NCC
    payment_status = Column(String(20), default='PAID') # PAID, DEBT
    note = Column(String(255), nullable=True)
    def to_dict(self):
        return {
            "import_id": self.import_id,
            "owner_id": self.owner_id,
            "supplier_id": self.supplier_id,
            "import_date": self.import_date.isoformat() if self.import_date else None,
            "total_amount": float(self.total_amount) if self.total_amount else 0,
            "payment_status": self.payment_status,
            "note": self.note
        }