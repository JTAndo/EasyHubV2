from db_utils import execute_query

class User: 
    def __init__(self, name, email, role):
        valid_roles = ["SuperAdmin", "Admin", "Non-Admin"]
        if role not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        self.name = name
        self.email = email
        self.role = role
    def save_to_db(self, cursor): 
        raise NotImplementedError("Subclasses must implement this method")
    
class SuperAdmin(User): 
    def __init__(self, name, email, permissions=None):
        super().__init__(name, email, "SuperAdmin")
        self.permissions = permissions or {}
    def save_to_db(self, cursor):
        
            query = """
            INSERT INTO admins (name, email, remote_access, video_call, voice_call, manage_users, is_super_admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
            """,
            params = (
                self.name,
                self.email,
                self.permissions.get("remote_access", True),
                self.permissions.get("video_call", True),
                self.permissions.get("voice_call", True),
                self.permissions.get("manage_users", True),
                True,  # is_super_admin
            ),
        
            return execute_query(query, params, fetch_one=True)

class Admin(User):
    def __init__(self, name, email, permissions=None):
        super().__init__(name, email, "Admin")
        self.permissions = permissions or {}

    def save_to_db(self, cursor):
        
            query ="""
            INSERT INTO admins (name, email, remote_access, video_call, voice_call, manage_users, is_super_admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
            """,
            params = (
                self.name,
                self.email,
                self.permissions.get("remote_access", False),
                self.permissions.get("video_call", False),
                self.permissions.get("voice_call", False),
                self.permissions.get("manage_users", False),
                False,  # is_super_admin
            ),
        
            return execute_query(query, params, fetch_one=True)


class NonAdmin(User):
    def __init__(self, name, email):
        super().__init__(name, email, "Non-Admin")

    def save_to_db(self, cursor):
        
            query = """
            INSERT INTO non_admins (name, email, family_member_count)
            VALUES (%s, %s, %s) RETURNING id
            """,
            params = (self.name, self.email, 0),
        
            return execute_query(query, params, fetch_one=True)