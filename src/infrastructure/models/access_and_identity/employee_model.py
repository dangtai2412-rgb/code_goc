from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from infrastructure.databases.base import Base

class EmployeeModel(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    employee_name = Column(String(100), nullable=False)
    # Bổ sung email để đăng nhập
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default='Staff') # Manager, Staff
    active_status = Column(Boolean, default=True)