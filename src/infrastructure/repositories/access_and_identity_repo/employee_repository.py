from infrastructure.models.access_and_identity.employee_model import EmployeeModel
from domain.models.employee import Employee
from infrastructure.databases.mssql import session

class EmployeeRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, emp):
        db_emp = EmployeeModel(
            employee_name=emp.employee_name,
            owner_id=emp.owner_id, # Chắc chắn có giá trị từ Token
            email=emp.email,
            password=emp.password,
            role=emp.role
        )
        self.session.add(db_emp)
        self.session.commit()
        self.session.refresh(db_emp)
        return db_emp

    def get_by_email(self, email: str):
        """Tìm nhân viên theo email để Login (chính xác hơn tên)"""
        return self.session.query(EmployeeModel).filter_by(email=email).first()

    def get_all(self):
        return self.session.query(EmployeeModel).all()

    def get_by_owner(self, owner_id):
        return self.session.query(EmployeeModel).filter_by(owner_id=owner_id).all()

    def get_by_name(self, name: str):
        """Giữ nguyên để tìm theo tên nếu cần"""
        return self.session.query(EmployeeModel).filter_by(employee_name=name).first()