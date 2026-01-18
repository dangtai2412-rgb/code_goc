from domain.models.business_owner import BusinessOwner
from werkzeug.security import generate_password_hash

class BusinessOwnerService:
    def __init__(self, repository):
        self.repository = repository

    def create_owner(self, data):
        # 1. Kiểm tra logic nghiệp vụ
        email = data.get('email')
        if not email or "@" not in email:
            raise ValueError("Email không hợp lệ!")

        phone = data.get('phone_number') # Khớp với key trong data gửi lên
        if not phone or len(phone) < 10:
            raise ValueError("Số điện thoại phải có ít nhất 10 chữ số!")

        # 2. Mã hóa mật khẩu trước khi lưu (Bảo mật)
        raw_password = data.get('password', '123456')
        hashed_password = generate_password_hash(raw_password)

        # 3. Đóng gói vào Domain
        new_owner_domain = BusinessOwner(
            owner_name=data.get('owner_name'),
            email=email,
            phone_number=phone,
            admin_id=data.get('admin_id'),
            plan_id=data.get('plan_id'),
            account_status=data.get('account_status', 'Active')
        )
        # Gán thêm password vào domain nếu domain có thuộc tính này
        new_owner_domain.password = hashed_password 
        
        return self.repository.add(new_owner_domain)

    def list_all_owners(self): # Tên hàm thống nhất
        return self.repository.get_all()