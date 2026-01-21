# src/infrastructure/repositories/ai_core_repo/ai_assistant_repository.py
from infrastructure.models.ai_core.ai_assistant_model import AIAssistantModel
from infrastructure.databases.mssql import session

class AIAssistantRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def update_config(self, version, model_type):
        """
        Lưu cấu hình AI mới vào database. 
        Nếu bạn muốn ghi đè cấu hình cũ, bạn có thể tìm bản ghi đầu tiên và update.
        """
        try:
            new_config = AIAssistantModel(
                version=version,
                ai_model_type=model_type,
                supported_languages="vi, en" # Giá trị mặc định
            )
            self.session.add(new_config)
            self.session.commit()
            self.session.refresh(new_config)
            return new_config
        except Exception as e:
            self.session.rollback()
            raise e

    def get_latest_config(self):
        """Lấy cấu hình AI mới nhất dựa trên ID giảm dần"""
        return self.session.query(AIAssistantModel).order_by(AIAssistantModel.ai_id.desc()).first()

    # Giữ lại các hàm cũ nếu cần
    def add(self, ai_model):
        self.session.add(ai_model)
        self.session.commit()
        return ai_model