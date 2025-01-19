import azure.functions as func
from azure.functions import FunctionApp
import psycopg2
import os
import json
import logging
from dotenv import load_dotenv
from models.users import SuperAdmin, Admin, NonAdmin
from db_utils import get_db_connection

app = func.FunctionApp()

@app.route(route="registerUser", auth_level=func.AuthLevel.ANONYMOUS)
def registerUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Registering user...")

    try:
        req_body = req.get_json()
        name = req_body.get("name")
        email = req_body.get("email")
        role = req_body.get("role")
        permissions = req_body.get("permissions", {})

        if not name or not email or not role:
            return func.HttpResponse(
                json.dumps(
                    {"error": "Missing required fields: name, email, or role."}
                ),
                status_code=400,
                mimetype="application/json",
            )

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                if role == "SuperAdmin":
                    super_admin = SuperAdmin(
                        name=name, email=email, permissions=permissions
                    )
                    admin_id = super_admin.save_to_db(cursor)
                    connection.commit()
                    logging.info("SuperAdmin added successfully.")
                    return func.HttpResponse(
                        json.dumps(
                            {
                                "message": f"Super Admin {name} registered successfully.",
                                "Admin ID": admin_id,
                            }
                        ),
                        status_code=201,
                        mimetype="application/json",
                    )
                elif role == "Admin":
                    admin = Admin(name=name, email=email, permissions=permissions)
                    admin_id = admin.save_to_db(cursor)
                    connection.commit()
                    logging.info("Admin added successfully.")
                    return func.HttpResponse(
                        json.dumps(
                            {
                                "message": f"Admin {name} registered successfully.",
                                "Admin ID": admin_id,
                            }
                        ),
                        status_code=201,
                        mimetype="application/json",
                    )
                elif role == "Non-Admin":
                    non_admin = NonAdmin(name=name, email=email)
                    non_admin_id = non_admin.save_to_db(cursor)
                    connection.commit()
                    logging.info("Non-Admin added successfully.")
                    return func.HttpResponse(
                        json.dumps(
                            {
                                "message": f"Non-Admin {name} registered successfully.",
                                "Non-Admin ID": non_admin_id,
                            }
                        ),
                        status_code=201,
                        mimetype="application/json",
                    )

    except psycopg2.IntegrityError:
        return func.HttpResponse(
            json.dumps({"error": "Email must be unique."}),
            status_code=400,
            mimetype="application/json",
        )
    except psycopg2.Error as e:
        logging.error("Unexpected database error: %s", str(e))
        return func.HttpResponse(
            json.dumps({"error": "Internal server error."}),
            status_code=500,
            mimetype="application/json",
        )
    except json.JSONDecodeError as e:
        logging.error("JSON decode error: %s", str(e))
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON format."}),
            status_code=400,
            mimetype="application/json",
        )
    except Exception as e:
        logging.error("Unexpected error: %s", str(e))
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
                cursor.execute("SELECT id, name, email, role FROM users")
                rows = cursor.fetchall()

        users = [
            {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "role": row[3]
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
