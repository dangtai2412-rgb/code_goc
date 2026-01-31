# src/init_db.py
from infrastructure.databases.mssql import engine
from infrastructure.databases.base import Base
# Import các model để SQLAlchemy nhận diện cấu trúc bảng
from infrastructure.models.access_and_identity.administrator_model import AdministratorModel
from infrastructure.models.access_and_identity.subscription_plan_model import SubscriptionPlanModel
from infrastructure.models.access_and_identity.business_owner_model import BusinessOwnerModel
from infrastructure.models.access_and_identity.employee_model import EmployeeModel

def initialize():
    print("--- Đang bắt đầu khởi tạo cấu trúc Database ---")
    try:
        # Lệnh này sẽ quét toàn bộ model và tạo bảng tương ứng trong SQL Server
        Base.metadata.create_all(bind=engine)
        print("--- Tạo các bảng thành công! ---")
    except Exception as e:
        print(f"--- Lỗi khi tạo bảng: {str(e)} ---")

if __name__ == "__main__":
    initialize()