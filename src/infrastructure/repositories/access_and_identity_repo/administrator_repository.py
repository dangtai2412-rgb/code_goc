from infrastructure.models.access_and_identity.administrator_model import AdministratorModel
from domain.models.administrator import Administrator
from infrastructure.databases.mssql import session

class AdministratorRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, admin: Administrator): # SỬA: Nhận đối tượng Domain thay vì tham số rời
        db_admin = AdministratorModel(
            admin_name=admin.admin_name, 
            email=admin.email,           # BỔ SUNG: Email
            admin_permission=admin.admin_permission,
            password=admin.password      # Lưu mật khẩu từ domain object
        )
        try:
            self.session.add(db_admin)
            self.session.commit()
            self.session.refresh(db_admin)
            return db_admin
        except Exception as e:
            self.session.rollback() 
            raise e

    def get_by_email(self, email: str):
        """Tìm Admin theo email"""
        return self.session.query(AdministratorModel).filter_by(email=email).first()

    def get_all(self):
        return self.session.query(AdministratorModel).all()

    def get_by_name(self, name):
        return self.session.query(AdministratorModel).filter_by(admin_name=name).first()