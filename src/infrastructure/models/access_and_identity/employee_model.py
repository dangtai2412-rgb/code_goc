from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from infrastructure.databases.base import Base

class EmployeeModel(Base):
    __tablename__ = 'employees'
    #__table_args__ = {'extend_existing': True}

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(100), nullable=False)
    role = Column(String(50))
    active_status = Column(Boolean, default=True)
    # Khóa ngoại: Nhân viên thuộc về một Business Owner
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))
    password = Column(String(255), nullable=False)