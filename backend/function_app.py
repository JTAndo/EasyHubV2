import azure.functions as func
from azure.functions import FunctionApp
import psycopg2
import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()
app = func.FunctionApp()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

@app.route(route="registerUser", auth_level=func.AuthLevel.ANONYMOUS)
def registerUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Registering user...")

    try:
        req_body = req.get_json()
        name = req_body.get("name")
        email = req_body.get("email")
        role = req_body.get("role")
        permissions = req_body.get("permissions", {})
        linked_admins = req_body.get("linked_admins", [])
        linked_non_admins = req_body.get("linked_non_admins", [])

        remote_access = permissions.get("remote_access", False)
        video_call = permissions.get("video_call", False)
        voice_call = permissions.get("voice_call", False)
        manage_users = permissions.get("manage_users", False)

        if not name or not email or not role:
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: name, email, or role."}),
                status_code=400,
                mimetype="application/json",
            )

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                if role == "Admin":
                    cursor.execute(
                        """
                        INSERT INTO admins (name, email, remote_access, video_call, voice_call, manage_users)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                        """,
                        (name, email, remote_access, video_call, voice_call, manage_users),
                    )
                    admin_id = cursor.fetchone()[0]
                    
                    if linked_non_admins:
                        for non_admin_email in linked_non_admins:
                            # Retrieve the Non-Admin ID
                            cursor.execute(
                                "SELECT id, name FROM non_admins WHERE email = %s",
                                (non_admin_email,)
                            )
                            non_admin_data = cursor.fetchone()
                            if non_admin_data:
                                non_admin_id, non_admin_name = non_admin_data
                                # Insert into admin_non_admin
                                cursor.execute(
                                    """
                                    INSERT INTO admin_non_admin (admin_id, non_admin_id, admin_email, name)
                                    VALUES (%s, %s, %s, %s)
                                    """,
                                    (admin_id, non_admin_id, email, non_admin_name)
                                )
                    connection.commit()
                    logging.info("Admin added successfully.")
                elif role == 'Non-Admin':
                    with get_db_connection() as connection:
                        with connection.cursor() as cursor:
                            # Insert the Non-Admin into the database
                            cursor.execute(
                                """
                                INSERT INTO non_admins (name, email, family_member_count)
                                VALUES (%s, %s, %s) RETURNING id
                                """,
                                (name, email, 0)
                            )
                            non_admin_id = cursor.fetchone()[0]

                            # Link to Admins if provided
                            if linked_admins:
                                for admin_email in linked_admins:
                                    # Retrieve the Admin ID
                                    cursor.execute(
                                        "SELECT id, name FROM admins WHERE email = %s",
                                        (admin_email,)
                                    )
                                    admin_data = cursor.fetchone()
                                    if admin_data:
                                        admin_id, admin_name = admin_data
                                        # Insert into admin_non_admin
                                        cursor.execute(
                                            """
                                            INSERT INTO admin_non_admin (admin_id, non_admin_id, admin_email, name)
                                            VALUES (%s, %s, %s, %s)
                                            """,
                                            (admin_id, non_admin_id, admin_email, name)
                                        )

                            connection.commit()

        return func.HttpResponse(
            json.dumps({"message": f"User {name} registered successfully.", "role": role}),
            status_code=201,
            mimetype="application/json",
        )

    except psycopg2.IntegrityError:
        return func.HttpResponse(
            json.dumps({"error": "Email must be unique."}),
            status_code=400,
            mimetype="application/json",
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error."}),
            status_code=500,
            mimetype="application/json",
        )
@app.route(route="linkAdminToNonAdmin", auth_level=func.AuthLevel.ANONYMOUS)
def linkAdminToNonAdmin(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        admin_email = req_body.get("admin_email")
        non_admin_email = req_body.get("non_admin_email")

        if not admin_email or not non_admin_email:
            return func.HttpResponse(
                json.dumps({"error": "Missing admin_email or non_admin_email."}),
                status_code=400,
                mimetype="application/json",
            )

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Get IDs
                cursor.execute("SELECT id FROM admins WHERE email = %s", (admin_email,))
                admin = cursor.fetchone()
                cursor.execute("SELECT id FROM non_admins WHERE email = %s", (non_admin_email,))
                non_admin = cursor.fetchone()

                if not admin or not non_admin:
                    return func.HttpResponse(
                        json.dumps({"error": "Admin or Non-Admin not found."}),
                        status_code=404,
                        mimetype="application/json",
                    )

                admin_id = admin[0]
                non_admin_id = non_admin[0]

                # Create link
                cursor.execute(
                    "INSERT INTO admin_non_admin (admin_id, non_admin_id, admin_email) VALUES (%s, %s, %s)",
                    (admin_id, non_admin_id, admin_email)
                )
                connection.commit()

        return func.HttpResponse(
            json.dumps({"message": "Admin linked to Non-Admin successfully."}),
            status_code=200,
            mimetype="application/json",
        )

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error."}),
            status_code=500,
            mimetype="application/json",
        )

@app.route(route="getUsers", auth_level=func.AuthLevel.ANONYMOUS)
def getUsers(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Getting users list...')
    
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email, role, permissions FROM users")
                rows = cursor.fetchall()

        users = [
            {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "role": row[3],
                "permissions": json.loads(row[4]) if row[4] else {}
            }
            for row in rows
        ]

        return func.HttpResponse(
            json.dumps(users),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error."}),
            status_code=500,
            mimetype="application/json"
        )
