from create_app import create_app
from infrastructure.databases import session
from infrastructure.models.access_and_identity.business_owner_model import BusinessOwnerModel
from infrastructure.models.access_and_identity.employee_model import EmployeeModel
from infrastructure.models.access_and_identity.subscription_plan_model import SubscriptionPlanModel
from werkzeug.security import generate_password_hash
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("--- BẮT ĐẦU TẠO DỮ LIỆU MẪU (BẢN FIX EMPLOYEE) ---")

    # BƯỚC 0: TẠO GÓI CƯỚC (Nếu chưa có)
    plan = session.query(SubscriptionPlanModel).filter_by(plan_name="Free Tier").first()
    if not plan:
        plan = SubscriptionPlanModel(
            plan_name="Free Tier",
            duration=365,
            price=0,
            description="Gói dùng thử miễn phí"
        )
        session.add(plan)
        session.commit()
        plan = session.query(SubscriptionPlanModel).filter_by(plan_name="Free Tier").first()

    # BƯỚC 1: TẠO CHỦ CỬA HÀNG (BUSINESS OWNER)
    owner = session.query(BusinessOwnerModel).filter_by(email="boss@bizflow.com").first()
    
    if not owner:
        new_owner = BusinessOwnerModel(
            owner_name="Chủ Cửa Hàng Demo",
            email="boss@bizflow.com",
            password=generate_password_hash("123456"), 
            phone_number="0901234567",
            plan_id=plan.plan_id
        )
        session.add(new_owner)
        session.commit()
        print("✅ 1. Đã tạo Business Owner")
        owner = session.query(BusinessOwnerModel).filter_by(email="boss@bizflow.com").first()
    else:
        print("ℹ️ Business Owner đã tồn tại.")

    # BƯỚC 2: TẠO NHÂN VIÊN (EMPLOYEE) - ID 1002
    try:
        # Kiểm tra nhân viên
        employee = session.get(EmployeeModel, 1002) 

        if not employee:
            session.execute(text("SET IDENTITY_INSERT employees ON"))
            
            # --- SỬA LỖI TẠI ĐÂY (Khớp với EmployeeModel bạn gửi) ---
            new_employee = EmployeeModel(
                employee_id=1002,
                
                # Model dùng 'email', không có 'username'
                email="staff_1002@bizflow.com", 
                
                # Model dùng 'employee_name', không phải 'full_name'
                employee_name="Nhân Viên Test AI", 
                
                # Model dùng 'password', không phải 'password_hash'
                password=generate_password_hash("123456"), 
                
                owner_id=owner.owner_id,
                role="Staff",
                active_status=True
            )
            session.add(new_employee)
            session.commit()
            
            session.execute(text("SET IDENTITY_INSERT employees OFF"))
            print("✅ 2. Đã tạo Employee ID 1002")
        else:
            print("ℹ️ Employee 1002 đã tồn tại.")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Lỗi khi tạo nhân viên: {e}")

    print("--- HOÀN TẤT! HÃY CHẠY LẠI APP.PY ---")