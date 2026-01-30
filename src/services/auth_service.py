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

    def _encode_token(self, payload):
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        if isinstance(token, bytes):
            return token.decode('utf-8')
        return token

    # SỬA: Thêm tham số role
    def login(self, email, password, role=None):
        user = None
        
        # Logic tìm user dựa trên Role được chọn
        if role == "admin":
            user = self.admin_repo.get_by_email(email)
        elif role == "owner":
            user = self.owner_repo.get_by_email(email)
        elif role == "employee":
            user = self.employee_repo.get_by_email(email)
        else:
            # Fallback: Nếu không chọn role thì tự động tìm (như cũ)
            user = self.admin_repo.get_by_email(email)
            role = "admin"
            if not user:
                user = self.owner_repo.get_by_email(email)
                role = "owner"
            if not user:
                user = self.employee_repo.get_by_email(email)
                role = "employee"

        if not user:
            return None

        # Kiểm tra mật khẩu
        if not check_password_hash(user.password, password):
            return None

        # Lấy ID (xử lý sự khác biệt tên cột giữa các bảng)
        user_id = getattr(user, 'id', None) or getattr(user, 'admin_id', None) or getattr(user, 'owner_id', None) or getattr(user, 'employee_id', None)
        
        # Nếu là nhân viên, cần lấy thêm owner_id của chủ
        owner_id = getattr(user, 'owner_id', None) if role != 'owner' else user_id

        # Tạo payload cho Token
        payload = {
            'user_id': user_id,
            'owner_id': owner_id,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }

        return {
            "token": self._encode_token(payload),
            "user": {
                "id": user_id,
                "name": getattr(user, 'name', None) or getattr(user, 'employee_name', None) or getattr(user, 'username', 'User'),
                "role": role
            }
        }