from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.models.access_and_identity.business_owner_model import BusinessOwnerModel
from domain.models.business_owner import BusinessOwner
from infrastructure.databases.mssql import session

class BusinessOwnerRepository:
    def __init__(self, session: Session = session):
        self.session = session

    # Giữ nguyên các phần import của bạn
    def add(self, owner: BusinessOwner) -> BusinessOwnerModel:
        try:
            db_owner = BusinessOwnerModel(
            owner_name=owner.owner_name,
            phone_number=owner.phone_number,
            email=owner.email,
            account_status=owner.account_status,
            admin_id=owner.admin_id,
            plan_id=owner.plan_id,
            password=owner.password # Cần lưu trường này để sau này Login
            )
            self.session.add(db_owner)
            self.session.commit()
            self.session.refresh(db_owner)
            return db_owner
        except Exception as e:
            self.session.rollback()
            raise e
    def get_by_name(self, name: str) -> Optional[BusinessOwnerModel]:
        """
        Tìm kiếm Chủ cửa hàng theo tên đăng nhập (owner_name)
        Phục vụ cho chiến thuật Auth quét 3 bảng.
        """
        return self.session.query(BusinessOwnerModel).filter_by(owner_name=name).first()
    def get_all(self) -> List[BusinessOwnerModel]:
        """Lấy toàn bộ danh sách chủ shop"""
        return self.session.query(BusinessOwnerModel).all()