from infrastructure.models.access_and_identity.administrator_model import AdministratorModel
from infrastructure.databases.mssql import session

class AdministratorRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, name, permission, hashed_password): # Thêm hashed_password
        db_admin = AdministratorModel(
            admin_name=name, 
            admin_permission=permission,
            password=hashed_password # Lưu mật khẩu vào DB
        )
        try:
            self.session.add(db_admin)
            self.session.commit()
            self.session.refresh(db_admin)
            return db_admin
        except Exception as e:
            self.session.rollback() # Cần thiết để tránh lỗi "transaction rolled back"
            raise e

    def get_all(self):
        return self.session.query(AdministratorModel).all()

    def get_by_name(self, name):
        return self.session.query(AdministratorModel).filter_by(admin_name=name).first()