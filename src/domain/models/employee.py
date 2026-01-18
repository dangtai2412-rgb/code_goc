class Employee:
    def __init__(self, employee_name, owner_id, role=None, active_status=True, employee_id=None):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.owner_id = owner_id # Khóa ngoại
        self.role = role
        self.active_status = active_status