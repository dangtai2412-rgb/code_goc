class Employee:
    def __init__(self, employee_name, owner_id, email, password, role=None, active_status=True, employee_id=None):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.owner_id = owner_id # Khóa ngoại
        self.email = email       # BỔ SUNG: Email để đăng nhập
        self.password = password # BỔ SUNG: Mật khẩu (thường là hash)
        self.role = role
        self.active_status = active_status