# login_history.py
# Tracks login/logout history for users in the Neyyal Billing System
from datetime import datetime
from typing import Optional
from utils.Tables import TableName as T
from utils.setup_db import create_login_history_table
from utils.DB_conn import execute_stmt, execute_stmt_return
from utils.session import clear_current_user

class LoginHistory:
    def __init__(self):
        """Initialize the LoginHistory class and create the login history table if it doesn't exist."""
        create_login_history_table()

    def record_login(self, user_id: int) -> None:
        """Record a user login event with the current timestamp and return the log ID."""
        login_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        execute_stmt(f'''
            INSERT INTO {T.LOGIN_HISTORY_TABLE.value} (user_id, login_time, logout_time)
            VALUES (?, ?, NULL)
            ''', (user_id, login_time))
        log_id = execute_stmt_return(f'''
            SELECT id FROM {T.LOGIN_HISTORY_TABLE.value}
            WHERE user_id = ? AND login_time = ?
            ORDER BY id DESC LIMIT 1
            ''', (user_id, login_time))[0][0]
        # Return the log ID for further processing
        return log_id


    def record_logout(self, log_id: int) -> None:
        clear_current_user()  # Clear the current user session
        """Record a user logout event with the current timestamp."""
        logout_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        execute_stmt(f'''
                UPDATE {T.LOGIN_HISTORY_TABLE.value}
                SET logout_time = ?
                WHERE id = ? AND logout_time IS NULL
                ORDER BY id DESC LIMIT 1
            ''', (logout_time, log_id))
        

    def get_user_history(self, user_id: int) -> list[tuple[str, Optional[str]]]:
        """Retrieve the login/logout history for a given user."""
        history: list[tuple[str, Optional[str]]] = execute_stmt_return(f'''
                SELECT login_time, logout_time FROM {T.LOGIN_HISTORY_TABLE.value}
                WHERE username = ? ORDER BY id DESC
            ''', (user_id,))
        return history
    
    def get_all_history(self) -> list[tuple[str, str | None]]:
        """Retrieve the complete login/logout history for all users."""
        history: list[tuple[str, str | None]] = execute_stmt_return(f'''
                SELECT id, login_time, logout_time FROM {T.LOGIN_HISTORY_TABLE.value}
                ORDER BY id DESC
            ''')
        return history

    def clear_history(self) -> None:
        """Clear the login/logout history table."""
        execute_stmt(f'DELETE FROM {T.LOGIN_HISTORY_TABLE.value}')
        print("Login history cleared.")