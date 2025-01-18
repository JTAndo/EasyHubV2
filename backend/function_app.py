import azure.functions as func
import psycopg2
import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

@app.route(route="registerUser", auth_level=func.AuthLevel.ANONYMOUS)
def registerUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Registering User...')
    
    try:
        req_body = req.get_json()
        name = req_body.get('name')
        email = req_body.get('email')
        role = req_body.get('role')
        permissions = req_body.get('permissions')

        if not name or not email or not role:
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields"}),
                status_code=400,
                mimetype="application/json"
            )
        
        permissions_json = json.dumps(permissions)

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email, role, permissions) VALUES (%s, %s, %s, %s)",
                    (name, email, role, permissions_json)
                )
                connection.commit()

        return func.HttpResponse(
            json.dumps({"message": f"User {name} registered successfully."}),
            status_code=201,
            mimetype="application/json"
        )

    except psycopg2.IntegrityError as e:
        return func.HttpResponse(
            json.dumps({"error": "Email must be unique."}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error."}),
            status_code=500,
            mimetype="application/json"
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
