from sqlalchemy import Column, Integer, String
from infrastructure.databases.base import Base

class AdministratorModel(Base):
    __tablename__ = 'administrators'

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_name = Column(String(100), nullable=False)
    # Bổ sung email để đăng nhập
    email = Column(String(100), unique=True, nullable=False)
    admin_permission = Column(String(100), default='SuperAdmin')
    password = Column(String(255), nullable=False)