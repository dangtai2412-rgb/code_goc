from domain.models.employee import Employee
from werkzeug.security import generate_password_hash # Dùng để mã hóa mật khẩu

class EmployeeService:
    def __init__(self, repository):
        self.repository = repository

    def create_employee(self, data):
        name = data.get('employee_name')
        if not name:
            raise ValueError("Tên nhân viên không được để trống")

        # 1. Mã hóa mật khẩu nhân viên
        raw_password = data.get('password', '123456') # Mặc định 123456 nếu trống
        hashed_password = generate_password_hash(raw_password)

        # 2. Đóng gói vào đối tượng Domain
        emp_domain = Employee(
            employee_name=name,
            owner_id=data.get('owner_id'),
            role=data.get('role', 'Staff'),
            active_status=data.get('active_status', True)
        )
        emp_domain.password = hashed_password # Gán mật khẩu đã mã hóa

        return self.repository.add(emp_domain)

    def get_employees_by_owner(self, owner_id):
        return self.repository.get_by_owner(owner_id)