from sqlalchemy import Column, Integer, String, Date, ForeignKey # Thêm ForeignKey
from infrastructure.databases.base import Base

class AccountReportModel(Base):
    __tablename__ = 'account_reports'
    #__table_args__ = {'extend_existing': True}
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    # Sửa lại dòng này để nối với bảng business_owners
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id')) 
    report_type = Column(String(50))
    reporting_period = Column(String(100))
    generated_date = Column(Date)