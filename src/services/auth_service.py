# src/services/auth_service.py
from werkzeug.security import check_password_hash
import jwt
import datetime

class AuthService:
    def __init__(self, admin_repo, owner_repo, employee_repo, secret_key):
        self.admin_repo = admin_repo
        self.owner_repo = owner_repo
        self.employee_repo = employee_repo
        self.secret_key = secret_key

    def login(self, email, password):
        user = self.admin_repo.get_by_email(email)
        role = "admin"
        
        if not user:
            user = self.owner_repo.get_by_email(email)
            role = "owner"
            
        if not user:
            user = self.employee_repo.get_by_email(email)
            role = "employee"

        if user and check_password_hash(user.password, password):
            # GIẢI PHÁP: Thử lấy 'id' trước (vì Domain Model thường dùng self.id)
            # Nếu không có mới thử các tên cụ thể khác
            user_id = getattr(user, 'id', None) or \
                      getattr(user, 'owner_id', None) or \
                      getattr(user, 'admin_id', None) or \
                      getattr(user, 'employee_id', None)
            
            # Nếu là chủ (owner) thì owner_id chính là user_id
            # Nếu là nhân viên, lấy owner_id từ bản ghi của họ (cột owner_id trong bảng Employees)
            owner_id = user_id if role == "owner" else getattr(user, 'owner_id', None)

            # Đóng gói Token
            payload = {
                'user_id': user_id,
                'owner_id': owner_id,
                'role': role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm="HS256")
            return token, role
            
        return None, None