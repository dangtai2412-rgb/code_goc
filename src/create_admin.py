from create_app import create_app
from infrastructure.databases import session 
from infrastructure.models.access_and_identity.administrator_model import AdministratorModel
from werkzeug.security import generate_password_hash
from app_logging import setup_logging
app = create_app()

with app.app_context():
    # 1. Thông tin Admin muốn tạo
    admin_email = "admin@bizflow.com" # Dùng email làm định danh chính
    admin_name = "Super Admin"
    password_raw = "123456"
    
    # 2. Kiểm tra xem email này đã tồn tại chưa (Vì ta đã đổi logic login sang Email)
    existing_user = session.query(AdministratorModel).filter_by(email=admin_email).first()
    
    if existing_user:
        print(f"❌ Tài khoản với email '{admin_email}' đã tồn tại rồi!")
    else:
        # 3. Mã hóa mật khẩu
        password_hash = generate_password_hash(password_raw)
        
        # 4. Lưu vào DB với đúng tên cột trong Model
        new_admin = AdministratorModel(
            admin_name=admin_name,         # Khớp với model.admin_name
            email=admin_email,             # Khớp với model.email
            password=password_hash,        # Khớp với model.password
            admin_permission="FullAccess"  # Thêm quyền mặc định
        )
        
        try:
            session.add(new_admin)
            session.commit()
            print(f"✅ Đã tạo tài khoản thành công!")
            print(f"   - Email đăng nhập: {admin_email}")
            print(f"   - Mật khẩu: {password_raw}")
        except Exception as e:
            session.rollback()
            print(f"❌ Có lỗi khi lưu vào Database: {str(e)}")