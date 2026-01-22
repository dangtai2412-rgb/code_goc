from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class SupplierModel(Base):
    __tablename__ = 'suppliers'

    # Khóa chính tự động tăng
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Khóa ngoại liên kết với chủ sở hữu doanh nghiệp
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    
    # Tên nhà cung cấp (bắt buộc)
    supplier_name = Column(String(100), nullable=False)
    
    # Số điện thoại liên lạc
    phone_number = Column(String(20), nullable=True)
    
    # Mã số thuế
    tax_code = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Supplier(id={self.supplier_id}, name='{self.supplier_name}')>"