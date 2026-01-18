from sqlalchemy import Column, Integer, String
from infrastructure.databases.base import Base
class AIAssistantModel(Base):
    __tablename__ = 'ai_assistants'
    #__table_args__ = {'extend_existing': True}
    ai_id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(20))
    supported_languages = Column(String(100))
    ai_model_type = Column(String(50))