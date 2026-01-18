class Administrator:
    def __init__(self, admin_name, admin_permission=None, admin_id=None):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.admin_permission = admin_permission