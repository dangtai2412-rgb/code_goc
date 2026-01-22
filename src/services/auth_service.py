
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
    # 1. Lấy ID của người đang đăng nhập
            user_id = getattr(user, 'admin_id', getattr(user, 'owner_id', getattr(user, 'employee_id', None)))
    
    # 2. Xác định owner_id: 
    # Nếu là chủ thì chính là user_id, nếu là nhân viên thì lấy owner_id từ bản ghi của họ
            owner_id = user_id if role == "owner" else getattr(user, 'owner_id', None)

    # 3. Đóng gói vào Token
            token = jwt.encode({
                'user_id': user_id,
                'owner_id': owner_id, # Đảm bảo khóa này tên là 'owner_id'
                'role': role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, self.secret_key, algorithm="HS256")
    
            return token, role
        return None, None