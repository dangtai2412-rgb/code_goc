from werkzeug.security import generate_password_hash
from infrastructure.models.access_and_identity.business_owner_model import BusinessOwnerModel

class BusinessOwnerService:
    def __init__(self, repository):
        self.repo = repository

    def create_owner(self, data):
        # Validate cơ bản
        if not data.get('email') or not data.get('password'):
            raise ValueError("Email và Password là bắt buộc")

        # Tự động gán Plan ID = 1 (Gói dùng thử) nếu không chọn
        plan_id = data.get('plan_id', 1)

        new_owner = BusinessOwnerModel(
            owner_name=data.get('owner_name'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
            account_status='Active',
            plan_id=plan_id,
            admin_id=None
        )
        return self.repo.add(new_owner)