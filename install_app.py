"""
install_app.py - Setup script for Angadi Billing System database and tables
"""

from utils.setup_db import Setup_DB

def install():
    db_setup = Setup_DB()
    # This will create the necessary tables in the database
    db_setup.create_tables()
    print("Database and tables created successfully.")

if __name__ == "__main__":
    install()
