from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from infrastructure.databases.base import Base

class AIDraftOrderModel(Base):
    __tablename__ = 'ai_draft_orders'
    
    # Giữ nguyên khóa chính
    draft_id = Column(Integer, primary_key=True, autoincrement=True)

    # --- SỬA LỖI MAPPING ---
    # Python dùng biến 'raw_text', nhưng sẽ lưu vào cột 'recognized_content' trong SQL
    raw_text = Column("recognized_content", Text, nullable=True)

    # Python dùng biến 'status', nhưng sẽ lưu vào cột 'confirmation_status' trong SQL
    status = Column("confirmation_status", String(30), default="Pending")
    
    # --- CÁC CỘT BỊ THIẾU TRONG DATABASE ---
    # (Lưu ý: Nếu bạn không chạy lệnh SQL ở bước 2, code vẫn sẽ lỗi ở dòng này)
    extracted_json = Column(Text, nullable=True) 

    # --- TIMESTAMPS ---
    # Nếu DB chưa có 2 cột này, bạn cần chạy SQL bước 2 để thêm, hoặc tạm thời comment lại để chạy được.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # --- KHÓA NGOẠI ---
    employee_id = Column(Integer, ForeignKey('employees.employee_id'), nullable=True)
    ai_id = Column(Integer, ForeignKey('ai_assistants.ai_id'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=True)

    # Cột 'source' có trong SQL nhưng chưa có trong Model, thêm vào để đồng bộ (optional)
    source = Column(String(50), nullable=True)