from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from infrastructure.databases.base import Base

class CustomerModel(Base):
    __tablename__ = 'customers'
    #__table_args__ = {'extend_existing': True}

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    address = Column(String(200))
    total_outstanding_debt = Column(Numeric(12, 2), default=0)
    
    # Khóa ngoại: Khách hàng của chủ cửa hàng nào
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))