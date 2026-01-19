from werkzeug.security import generate_password_hash
from domain.models.employee import Employee

class EmployeeService:
    def __init__(self, employee_repo):
        self.employee_repo = employee_repo

    def create_employee(self, data):
        # Kiểm tra email tồn tại
        if self.employee_repo.get_by_email(data['email']):
            raise Exception("Email đã tồn tại")

        # Mã hóa mật khẩu
        hashed_pw = generate_password_hash(data['password'])

        # Tạo Domain Object
        new_emp = Employee(
            employee_name=data['employee_name'],
            owner_id=data['owner_id'],
            email=data['email'],
            password=hashed_pw, # Lưu mật khẩu đã mã hóa
            role=data.get('role'),
            active_status=True
        )
        return self.employee_repo.add(new_emp)