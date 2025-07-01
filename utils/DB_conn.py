# DB_Conn.py
# Centralized database connection utility for Angadi

import sqlite3
import logging
from typing import Any
from configuration import DB_PATH
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

def execute_stmt(stmt: str, params: tuple[Any, ...] = ()) -> bool:
    """
    Executes a parameterized SQL statement to ensure the connection is working.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(stmt, params)
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e} \nStatement: {stmt} \nParams: {params}")
        return False
    return True

def execute_stmt_return(stmt: str, params: tuple[Any, ...] = ()) -> list[tuple[str, Any | None]]:
    """
    Executes a parameterized SQL statement and returns the result.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(stmt, params)
            result = cursor.fetchall()
            return result
    except sqlite3.Error as e:
        logging.error(f"Database error: {e} \nStatement: {stmt} \nParams: {params}")
        return []

def close_connection(conn: sqlite3.Connection) -> None:
    """
    Closes the given SQLite connection.
    """
    if conn:
        conn.close()
        logging.info("Database connection closed.")
    else:
        logging.warning("Attempted to close a None connection.")


def execute_stmt_return_one(stmt: str, params: tuple[Any, ...] = ()) -> tuple[Any, ...] | None:
    """
    Executes a parameterized SQL statement and returns the result.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(stmt, params)
            result = cursor.fetchone()
            return result
    except sqlite3.Error as e:
        logging.error(f"Database error: {e} \nStatement: {stmt} \nParams: {params}")
        return (None,)