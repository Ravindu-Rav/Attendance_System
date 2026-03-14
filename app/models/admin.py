class Admin:
    def __init__(self, admin_id, username, password, created_at=None):
        self.admin_id = admin_id
        self.username = username
        self.password = password
        self.created_at = created_at