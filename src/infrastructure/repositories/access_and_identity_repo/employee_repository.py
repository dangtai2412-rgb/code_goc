from infrastructure.models.access_and_identity.employee_model import EmployeeModel
from domain.models.employee import Employee
from infrastructure.databases.mssql import session

class EmployeeRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, emp: Employee):
        try:
            db_emp = EmployeeModel(
                employee_name=emp.employee_name,
                owner_id=emp.owner_id,
                role=emp.role,
                active_status=emp.active_status,
                password=emp.password # BỔ SUNG: Lưu mật khẩu vào DB
            )
            self.session.add(db_emp)
            self.session.commit()
            self.session.refresh(db_emp)
            return db_emp
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self):
        return self.session.query(EmployeeModel).all()

    def get_by_owner(self, owner_id):
        return self.session.query(EmployeeModel).filter_by(owner_id=owner_id).all()

    def get_by_name(self, name: str):
        """Tìm nhân viên theo tên để phục vụ Login"""
        return self.session.query(EmployeeModel).filter_by(employee_name=name).first()