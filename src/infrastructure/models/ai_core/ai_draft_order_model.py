from sqlalchemy import Column, Integer, String, Text, ForeignKey
from infrastructure.databases.base import Base
class AIDraftOrderModel(Base):
    __tablename__ = 'ai_draft_orders'
    #__table_args__ = {'extend_existing': True}
    draft_id = Column(Integer, primary_key=True, autoincrement=True)
    recognized_content = Column(Text)
    confirmation_status = Column(String(20))
    source = Column(String(50))
    # Các khóa ngoại
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    ai_id = Column(Integer, ForeignKey('ai_assistants.ai_id'))
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))