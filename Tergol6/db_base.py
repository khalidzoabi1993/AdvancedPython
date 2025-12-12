# file: db_base.py

import configparser
from sqlalchemy import create_engine, MetaData, text

# ---------- Settings ----------

DB_NAME = "student_system"


# ---------- Config & Connection Helpers ----------

def get_db_config():
    """
    Reads MySQL connection details from config.ini
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    return {
        "host": config["mysql"]["host"],
        "user": config["mysql"]["user"],
        "password": config["mysql"]["password"],
    }


def get_server_engine():
    """
    Returns an engine connected to the MySQL server (without specific DB).
    Used only for CREATE DATABASE.
    """
    db = get_db_config()
    server_url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}"
    engine = create_engine(server_url, echo=True, future=True)
    return engine


def create_database_if_not_exists():
    """
    Creates the database if it does not exist yet.
    """
    server_engine = get_server_engine()
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        print(f"Database '{DB_NAME}' created (or already exists).")


def get_engine():
    """
    Returns an engine connected to the specific database (student_system).
    Ensures the database exists first.
    """
    create_database_if_not_exists()
    db = get_db_config()
    db_url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}/{DB_NAME}"
    engine = create_engine(db_url, echo=True, future=True)
    return engine


# ---------- Global objects to be reused in other files ----------

# metadata: will hold table definitions (students, courses, etc.)
metadata = MetaData()

# engine: connection manager to the specific DB
engine = get_engine()


def create_all_tables():
    """
    Creates all tables registered in 'metadata'.
    Does NOT drop or override existing tables.
    """
    metadata.create_all(engine)
    print("All tables in metadata were created (if not existing).")


def get_connection():
    """
    Returns a connection object you can use with engine.connect()
    """
    return engine.connect()


# Small demo when running this file directly (optional)
if __name__ == "__main__":
    # Just ensure DB exists and connection works
    with get_connection() as conn:
        result = conn.execute(text("SELECT DATABASE()"))
        db_name = result.scalar_one()
        print(f"Connected to database: {db_name}")
