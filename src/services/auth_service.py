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
        # 1. Quét bảng Admin
        user = self.admin_repo.get_by_email(email)
        role = "admin"
        
        # 2. Nếu không thấy, quét bảng BusinessOwner
        if not user:
            user = self.owner_repo.get_by_email(email)
            role = "owner"
            
        # 3. Nếu vẫn không thấy, quét bảng Employee
        if not user:
            user = self.employee_repo.get_by_email(email)
            role = "employee"

        # Kiểm tra user và mật khẩu
        if user and check_password_hash(user.password, password):
        # Lấy ID của user hiện tại
            current_id = getattr(user, 'admin_id', getattr(user, 'owner_id', getattr(user, 'employee_id', None)))
        
        # Xác định owner_id (Nếu là chủ thì là chính họ, nếu là nhân viên thì lấy owner_id của họ)
            owner_id = current_id if role == "owner" else getattr(user, 'owner_id', None)

            token = jwt.encode({
                'user_id': current_id,
                'owner_id': owner_id, # BỔ SUNG DÒNG NÀY
                'role': role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, self.secret_key, algorithm="HS256")
        
            return token, role
        return None, None