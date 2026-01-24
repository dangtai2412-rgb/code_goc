from infrastructure.models.ai_core.ai_draft_order_model import AIDraftOrderModel
from infrastructure.databases.mssql import session  # Note: adjust import if using other DB adapters
import json
from sqlalchemy.exc import SQLAlchemyError

class AIDraftOrderRepository:
    def __init__(self, db_session=session):
        # use session provider injected via dependency container in runtime
        self.session = db_session

    def add(self, draft: AIDraftOrderModel):
        try:
            self.session.add(draft)
            self.session.commit()
            self.session.refresh(draft)
            return draft
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def create_draft(self, raw_text, extracted_json=None, employee_id=None, ai_id=None, customer_id=None, status="Pending"):
        """Lưu kết quả AI bóc tách được vào DB.
        extracted_json can be dict or JSON string. We will store JSON string.
        """
        try:
            json_str = json.dumps(extracted_json) if extracted_json is not None and not isinstance(extracted_json, str) else (extracted_json or None)
            new_draft = AIDraftOrderModel(
                raw_text=raw_text,
                extracted_json=json_str,
                status=status,
                employee_id=employee_id,
                ai_id=ai_id,
                customer_id=customer_id
            )
            self.session.add(new_draft)
            self.session.commit()
            self.session.refresh(new_draft)
            return new_draft
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def get_by_id(self, draft_id):
        return self.session.query(AIDraftOrderModel).filter_by(draft_id=draft_id).first()

    def get_pending_drafts(self):
        return self.session.query(AIDraftOrderModel).filter_by(status="Pending").order_by(AIDraftOrderModel.created_at.desc()).all()

    def update_status(self, draft_id, status):
        draft = self.get_by_id(draft_id)
        if draft:
            try:
                draft.status = status
                self.session.commit()
                self.session.refresh(draft)
            except Exception:
                self.session.rollback()
                raise
        return draft