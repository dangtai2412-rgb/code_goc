from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from infrastructure.databases.base import Base

class AIDraftOrderModel(Base):
    __tablename__ = 'ai_draft_orders'
    draft_id = Column(Integer, primary_key=True, autoincrement=True)

    # raw_text: nội dung gốc (text/voice) mà AI phân tích
    raw_text = Column(Text, nullable=False)

    # extracted_json: JSON string lưu kết quả trích xuất từ LLM (items, customer_name, payment_method, confidence)
    extracted_json = Column(Text, nullable=True)

    # status: Pending | Confirmed | Rejected | Error
    status = Column(String(30), default="Pending")

    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # khóa ngoại — nếu cần
    employee_id = Column(Integer, ForeignKey('employees.employee_id'), nullable=True)
    ai_id = Column(Integer, ForeignKey('ai_assistants.ai_id'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=True)