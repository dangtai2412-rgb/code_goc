from infrastructure.models.ai_core.ai_assistant_model import AIAssistantModel
from domain.models.ai_assistant import AIAssistant
from infrastructure.databases.mssql import session

class AIAssistantRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, ai: AIAssistant):
        try:
            db_ai = AIAssistantModel(
                version=ai.version,
                supported_languages=ai.supported_languages,
                ai_model_type=ai.ai_model_type
            )
            self.session.add(db_ai)
            self.session.commit()
            self.session.refresh(db_ai)
            return db_ai
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self):
        return self.session.query(AIAssistantModel).all()