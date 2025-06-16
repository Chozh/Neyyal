# login_history.py
# Tracks login/logout history for users in the Angadi Billing System
from datetime import datetime
from typing import Optional
from utils.Tables import TableName as T
from utils.setup_db import create_login_history_table
from utils.DB_conn import execute_stmt, execute_stmt_return

class LoginHistory:
    def __init__(self):
        """Initialize the LoginHistory class and create the login history table if it doesn't exist."""
        create_login_history_table()

    def record_login(self, username: str) -> None:
        login_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        execute_stmt(f'''
            INSERT INTO {T.LOGIN_HISTORY_TABLE} (username, login_time, logout_time)
            VALUES (?, ?, NULL)
            ''', (username, login_time))


    def record_logout(self, username: str):
        logout_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        execute_stmt(f'''
                UPDATE {T.LOGIN_HISTORY_TABLE}
                SET logout_time = ?
                WHERE username = ? AND logout_time IS NULL
                ORDER BY id DESC LIMIT 1
            ''', (logout_time, username))
        

    def get_user_history(self, username: str) -> list[tuple[str, Optional[str]]]:
        """Retrieve the login/logout history for a given user."""
        history: list[tuple[str, Optional[str]]] = execute_stmt_return(f'''
                SELECT login_time, logout_time FROM {T.LOGIN_HISTORY_TABLE}
                WHERE username = ? ORDER BY id DESC
            ''', (username,))
        return history
    
    def get_all_history(self) -> list[tuple[str, str | None]]:
        """Retrieve the complete login/logout history for all users."""
        history: list[tuple[str, str | None]] = execute_stmt_return(f'''
                SELECT username, login_time, logout_time FROM {T.LOGIN_HISTORY_TABLE}
                ORDER BY id DESC
            ''')
        return history

