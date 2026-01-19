class Administrator:
    def __init__(self, admin_name, email, password, admin_permission=None, admin_id=None):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.email = email       # BỔ SUNG: Email để đăng nhập
        self.password = password # BỔ SUNG: Mật khẩu
        self.admin_permission = admin_permission