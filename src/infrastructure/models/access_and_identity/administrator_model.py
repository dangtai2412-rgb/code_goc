from sqlalchemy import Column, Integer, String
from infrastructure.databases.base import Base

class AdministratorModel(Base):
    __tablename__ = 'administrators'
    #__table_args__ = {'extend_existing': True}

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_name = Column(String(100), nullable=False)
    admin_permission = Column(String(100))
    password = Column(String(255), nullable=False)