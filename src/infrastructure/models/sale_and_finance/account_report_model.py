from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from infrastructure.databases.base import Base

class AccountReportModel(Base):
    __tablename__ = 'account_reports'

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'), nullable=False)
    
    # TT88_Revenue (Sổ doanh thu), TT88_Inventory (Sổ vật tư)
    report_type = Column(String(50), nullable=False)
    reporting_period = Column(String(100)) # VD: "Tháng 01/2026"
    file_path = Column(String(255), nullable=True) # Đường dẫn file PDF/Excel nếu có
    generated_date = Column(DateTime(timezone=True), server_default=func.now())