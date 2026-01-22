from werkzeug.security import generate_password_hash
from domain.models.employee import Employee

class EmployeeService:
    def __init__(self, employee_repo):
        self.employee_repo = employee_repo

    def create_employee(self, data, owner_id): # Thêm tham số owner_id
        if self.employee_repo.get_by_email(data['email']):
            raise Exception("Email đã tồn tại")

        # Giả sử bạn có import domain Employee
        new_emp = Employee(
            employee_name=data['employee_name'],
            owner_id=owner_id, # Dùng owner_id từ Token
            email=data['email'],
            password=generate_password_hash(data['password']),
            role=data.get('role', 'Staff')
        )
        return self.employee_repo.add(new_emp)

    def get_employees_by_owner(self, owner_id):
        return self.employee_repo.get_by_owner(owner_id)