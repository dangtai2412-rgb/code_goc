from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.databases.base import Base

class CategoryModel(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    category_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)