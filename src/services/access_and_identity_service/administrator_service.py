from werkzeug.security import generate_password_hash

class AdministratorService:
    def __init__(self, repository):
        self.repository = repository

    def create_admin(self, data):
        if not data.get('admin_name') or not data.get('password'):
            raise ValueError("Tên và Mật khẩu là bắt buộc")
            
        # 1. Mã hóa mật khẩu để bảo mật
        hashed_pw = generate_password_hash(data['password'])
        
        # 2. Gửi xuống Repo
        return self.repository.add(
            data['admin_name'], 
            data['admin_permission'], 
            hashed_pw
        )

    def get_all_admins(self):
        return self.repository.get_all()