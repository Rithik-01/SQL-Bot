import pandas as pd
from sqlalchemy import create_engine,text
from config import DB_URL
import pymysql
pymysql.install_as_MySQLdb()

def get_connection():
    """Create and return a MySQL DB connection."""
    return create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args={
        "connect_timeout": 30,
        "ssl": {"fake_flag_to_enable_tls": True}  # enable SSL if required
    }
    )

def get_tables():
    """Return a list of all tables in the database."""
    conn = get_connection()
    cursor = conn.connect()
    result=cursor.execute(text("SHOW TABLES"))
    tables = [row[0] for row in result]
    cursor.close()
    return tables

def get_columns(table_name: str):
    """Return all columns for a given table."""
    conn = get_connection()
    cursor = conn.connect()
    result=cursor.execute(text(f"SHOW COLUMNS FROM {table_name}"))
    cols = [row[0] for row in result]
    cursor.close()
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


def get_table_details():
    """Fetch tables, columns, and sample rows from the database using SQLAlchemy."""
    
    engine = get_connection()
    database_schema = {"database": engine.url.database, "tables": []}

    # Get list of tables
    tables = get_tables()  

    with engine.connect() as conn:
        for table in tables:
            table_info = {"name": table, "columns": []}

            # Get column info
            col_query = text(f"""
                SELECT COLUMN_NAME, COLUMN_TYPE, DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = :db
                AND TABLE_NAME = :table;
            """)
            columns = conn.execute(col_query, {"db": engine.url.database, "table": table}).fetchall()

            # Get one sample row
            sample_query = text(f"SELECT * FROM {table} LIMIT 1;")
            rows = pd.read_sql(sample_query, conn)

            # Build column details
            for col in columns:
                example_value = rows.iloc[0][col.COLUMN_NAME] if not rows.empty else None
                table_info["columns"].append({
                    "name": col.COLUMN_NAME,
                    "type": col.COLUMN_TYPE,
                    "ex_data": example_value
                })

            table_info["sample_rows"] = rows.to_dict(orient="records")
            database_schema["tables"].append(table_info)

    return database_schema


def run_multiple_query(query:str)-> pd.DataFrame:
    """Execute one or more SQL queries on the DB."""
    engine = get_connection()  
    conn = engine.connect()    
    df = None

    result = conn.execute(text(query))
    if result.returns_rows:
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

    conn.commit()
    conn.close()

    return df
