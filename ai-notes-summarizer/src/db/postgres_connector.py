# filepath: ai-notes-summarizer/ai-notes-summarizer/src/db/postgres_connector.py

import psycopg2
from psycopg2 import sql

def connect_to_db(host, database, user, password):
    """Establishes a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        print("Connection to the database established successfully.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(connection, query, params=None):
    """Executes a given SQL query using the provided connection."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
            print("Query executed successfully.")
    except Exception as e:
        print(f"Error executing query: {e}")

def fetch_results(connection, query, params=None):
    """Fetches results from the database for a given SQL query."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error fetching results: {e}")
        return None

def close_connection(connection):
    """Closes the database connection."""
    if connection:
        connection.close()
        print("Database connection closed.")