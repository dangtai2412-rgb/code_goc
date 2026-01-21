from werkzeug.security import generate_password_hash
from domain.models.business_owner import BusinessOwner # SỬA: Dùng Domain thay vì Model

class BusinessOwnerService:
    def __init__(self, repository):
        self.repo = repository

    def create_owner(self, data):
        # 1. Validate và kiểm tra tồn tại
        if not data.get('email') or not data.get('password'):
            raise ValueError("Email và Password là bắt buộc")
            
        if self.repo.get_by_email(data['email']):
            raise Exception("Email chủ cửa hàng đã tồn tại")

        # 2. Xử lý logic nghiệp vụ (Gói cước mặc định)
        plan_id = data.get('plan_id', 1)

        # 3. Mã hóa mật khẩu
        hashed_pw = generate_password_hash(data.get('password'))

        # 4. Tạo Domain Object (Thay vì BusinessOwnerModel)
        new_owner = BusinessOwner(
            owner_name=data.get('owner_name'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            password=hashed_pw,
            account_status='Active',
            plan_id=plan_id,
            admin_id=None
        )
        return self.repo.add(new_owner)
    def list_all_owners(self):
        """Lấy danh sách tất cả chủ cửa hàng"""
        return self.repo.get_all()