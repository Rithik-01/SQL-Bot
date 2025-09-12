import mysql.connector
import pandas as pd
from src.config import DB_NAME,DB_HOST,DB_PASSWORD, DB_USER

def get_connection():
    """Create and return a MySQL DB connection."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def get_tables():
    """Return a list of all tables in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tables

def get_columns(table_name: str):
    """Return all columns for a given table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    cols = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return cols

def get_schema_description():
    """Fetch tables and columns, return as text."""
    schema_text = "Database Schema:\n"
    tables = get_tables()
    for t in tables:
        cols = get_columns(t)
        schema_text += f"- {t} ({', '.join(cols)})\n"
    return schema_text

def is_safe_query(query: str) -> bool:
    """Check if the SQL query is allowed."""
    query_lower = query.strip().lower()

    forbidden = ["drop database", "shutdown", "truncate", "grant", "revoke"]
    for word in forbidden:
        if word in query_lower:
            return False
    return True

def run_query(query: str):
    """Execute a SQL query on the DB."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query , multi=True)

    if query.strip().lower().startswith("select"):
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return pd.DataFrame(rows, columns=columns)
    
    conn.commit()
    cursor.close()
    conn.close()
    return None

def run_multiple_query(query:str)-> pd.DataFrame:
    """Execute one or more SQL queries on the DB."""
    conn = get_connection()
    results = []

    with conn.cursor() as cursor:
        cursor.execute(query, map_results=True)

        for statement, result_set in cursor.fetchsets():
            if result_set: 
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(result_set, columns=columns)
                results.append(df)

    conn.commit()
    conn.close()

    return results[0]
