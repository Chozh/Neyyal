"""
install_app.py - Setup script for Neyyal Billing System database and tables
"""

from utils.setup_db import Setup_DB
from utils.Tables import TableName as T
from utils.DB_conn import execute_stmt, execute_stmt_return

def install():
    db_setup = Setup_DB()
    # This will create the necessary tables in the database
    db_setup.create_tables()
    print("Database and tables created successfully.")

def add_super_user(
    name: str = "Super User",
    username: str = "admin",
    phone: str = "1234567890",
    address: str = "HQ",
    password: str = "admin",
    user_type: str = "SUPER",
    added_by: int = 1  # Assuming the super user is added by itself
) -> None:
    """Add a super user (admin) to the users table if not already present."""
    # Check if super user already exists
    if execute_stmt_return(f"SELECT id FROM {T.USERS_TABLE.value} WHERE username = ?", (username,)) != []:
        print(f"Super user '{username}' already exists.")
    else:
        execute_stmt(
            "INSERT INTO users (name, username, phone, address, password, user_type, added_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, username, phone, address, password, user_type, added_by)
        )
        print(f"Super user '{username}' added successfully.")

def drop_table(table_name: str) -> None:
    """Drop a table from the database if it exists."""
    try:
        execute_stmt(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Table '{table_name}' dropped successfully.")
    except Exception as e:
        print(f"Error dropping table '{table_name}': {e}")

if __name__ == "__main__":
    drop_table(T.USERS_TABLE.value)  # Drop users table if it exists
    install()
    add_super_user()
