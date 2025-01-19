from db_utils import execute_query

class RelationshipManager:
    @staticmethod
    def link_admin_to_non_admin(admin_email, non_admin_email):
        """
        Link an Admin to a Non-Admin in the `admin_non_admin` table.
        Args:
            admin_email (str): Email of the Admin.
            non_admin_email (str): Email of the Non-Admin.
        Returns:
            dict: Success or error message.
        """
        # Fetch IDs for admin and non-admin
        admin_query = "SELECT id FROM admins WHERE email = %s"
        non_admin_query = "SELECT id FROM non_admins WHERE email = %s"

        admin_id = execute_query(admin_query, (admin_email,), fetch_one=True)
        non_admin_id = execute_query(non_admin_query, (non_admin_email,), fetch_one=True)

        if not admin_id or not non_admin_id:
            return {"error": "Admin or Non-Admin not found."}

        # Insert the relationship
        insert_query = """
            INSERT INTO admin_non_admin (admin_id, non_admin_id, admin_email)
            VALUES (%s, %s, %s)
        """
        try:
            execute_query(insert_query, (admin_id[0], non_admin_id[0], admin_email))
            return {"message": "Admin linked to Non-Admin successfully."}
        except Exception as e:
            return {"error": f"Failed to link: {str(e)}"}
