import mysql.connector
import pandas as pd
from config import DB_NAME,DB_HOST,DB_PASSWORD, DB_USER

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

def get_table_details():
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    tables=get_tables()
    
    database_schema = {
        "database": conn.database,
        "tables": []
    }
    for table in tables:
        
        table_info = {"name": table, "columns": []}

        cursor.execute(f"""
            SELECT COLUMN_NAME, COLUMN_TYPE, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{conn.database}'
            AND TABLE_NAME = '{table}';
        """)
        columns = cursor.fetchall()

        cursor.execute(f"SELECT * FROM {table} LIMIT 1;")
        rows = cursor.fetchall()

        for col in columns:
            table_info["columns"].append({
                "name": col["COLUMN_NAME"],
                "type": col["COLUMN_TYPE"],
                "ex_data":rows[0][col["COLUMN_NAME"]]
            })

        table_info["sample_rows"] = rows
        database_schema["tables"].append(table_info)

    conn.commit()
    conn.close()
    return database_schema

def run_multiple_query(query:str)-> pd.DataFrame:
    """Execute one or more SQL queries on the DB."""
    conn = get_connection()
    df = None

    with conn.cursor() as cursor:
        cursor.execute(query, map_results=True)

        for statement, result_set in cursor.fetchsets():
            if result_set: 
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(result_set, columns=columns)
                

    conn.commit()
    conn.close()

    return df
