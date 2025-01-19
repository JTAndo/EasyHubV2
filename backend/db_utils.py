import psycopg2
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Database connection configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", 5432),
}

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database using the configuration.
    Returns:
        psycopg2.connection: The database connection object.
    """
    try:
        logging.info("Database configuration: %s", {k: v for k, v in DB_CONFIG.items() if k != "password"})
        connection = psycopg2.connect(**DB_CONFIG)
        logging.info("Connected to the database.")
        return connection
    except psycopg2.Error as e:
        raise Exception(f"BOOOOOO Error connecting to database: {str(e)}")

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a SQL query with optional parameters.
    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): The parameters for the query.
        fetch_one (bool, optional): Whether to fetch a single result.
        fetch_all (bool, optional): Whether to fetch all results.
    Returns:
        list | dict | None: Query result, depending on fetch flags.
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            connection.commit()
            return None
