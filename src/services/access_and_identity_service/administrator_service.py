from werkzeug.security import generate_password_hash
from domain.models.administrator import Administrator # Bổ sung import

class AdministratorService:
    def __init__(self, repository):
        self.repository = repository

    def create_admin(self, data):
        # 1. Kiểm tra dữ liệu đầu vào
        if not data.get('admin_name') or not data.get('password') or not data.get('email'):
            raise ValueError("Tên, Email và Mật khẩu là bắt buộc")
            
        # 2. Kiểm tra email tồn tại
        if self.repository.get_by_email(data['email']):
            raise Exception("Email admin này đã tồn tại")

        # 3. Mã hóa mật khẩu
        hashed_pw = generate_password_hash(data['password'])
        
        # 4. Tạo Domain Object và gửi xuống Repo
        new_admin = Administrator(
            admin_name=data['admin_name'],
            email=data['email'],
            password=hashed_pw,
            admin_permission=data.get('admin_permission')
        )
        return self.repository.add(new_admin) # Gửi domain object

    def get_all_admins(self):
        return self.repository.get_all()