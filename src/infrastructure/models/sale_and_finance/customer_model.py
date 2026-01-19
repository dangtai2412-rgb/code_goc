from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from infrastructure.databases.base import Base

class CustomerModel(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    # Ràng buộc chặt chẽ với chủ cửa hàng
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    customer_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    email = Column(String(100), nullable=True)
    # Lưu tổng nợ hiện tại để truy vấn nhanh
    total_outstanding_debt = Column(Numeric(12, 2), default=0)