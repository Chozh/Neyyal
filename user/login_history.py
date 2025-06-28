# login_history.py
# Tracks login/logout history for users in the Neyyal Billing System

from datetime import datetime
from typing import Optional, List
from utils.Tables import TableName as T
from utils.setup_db import create_login_history_table
from utils.DB_conn import execute_stmt, execute_stmt_return_one, execute_stmt_return
from user.session import clear_current_session, set_current_session, get_current_user_name

class LoginHistoryRecord:
    """Represents a single login/logout record."""
    def __init__(self, session_id: int, username: str, login_time: str, logout_time: Optional[str]):
        self.session_id = session_id
        self.username = username
        self.login_time = login_time
        self.logout_time = logout_time

    def __repr__(self):
        return (f"LoginHistoryRecord(session_id={self.session_id}, username='{self.username}', "
                f"login_time='{self.login_time}', logout_time='{self.logout_time}')")

class LoginHistory:
    """Handles login/logout history operations."""

    def __init__(self):
        """Initialize the LoginHistory class and create the login history table if it doesn't exist."""
        create_login_history_table()

    def record_login(self, username: str) -> int:
        """Record a user login event with the current timestamp and return the session_id."""
        login_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        execute_stmt(f'''
            INSERT INTO {T.LOGIN_HISTORY_TABLE.value} (username, login_time, logout_time)
            VALUES (?, ?, NULL)
            ''', (username, login_time))
        result = execute_stmt_return_one(f'''
            SELECT session_id FROM {T.LOGIN_HISTORY_TABLE.value}
            WHERE username = ? AND login_time = ?
            ORDER BY session_id DESC LIMIT 1
            ''', (username, login_time))
        if result and result[0]:
            session_id: int = result[0]
            set_current_session(username, session_id)
            return session_id
        else:
            raise ValueError("Failed to retrieve session_id for the login event.")

    @staticmethod
    def record_logout(session_id: int) -> None:
        """Record a user logout event with the current timestamp."""
        clear_current_session()  # Clear the current session_id
        logout_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        if execute_stmt(f'''
                UPDATE {T.LOGIN_HISTORY_TABLE.value}
                SET logout_time = ?
                WHERE session_id = ? AND logout_time IS NULL
            ''', (logout_time, session_id)) is False:
            raise ValueError(f"Logout Failed! Failed for the User: {get_current_user_name()} (session_id={session_id})")

    def get_user_history(self, username: str) -> List[LoginHistoryRecord]:
        """Retrieve the login/logout history for a given user as a list of LoginHistoryRecord objects."""
        rows = execute_stmt_return(f'''
                SELECT session_id, username, login_time, logout_time FROM {T.LOGIN_HISTORY_TABLE.value}
                WHERE username = ? ORDER BY session_id DESC
            ''', (username,))
        return [
            LoginHistoryRecord(
                session_id=int(row[0]),
                username=str(row[1]) if row[1] is not None else "",
                login_time=str(row[2]) if len(row) > 2 and row[2] is not None else "",
                logout_time=str(row[3]) if len(row) > 3 and row[3] is not None else None
            )
            for row in rows if len(row) >= 4
        ]

    def get_all_history(self) -> List[LoginHistoryRecord]:
        """Retrieve the complete login/logout history for all users as a list of LoginHistoryRecord objects."""
        rows = execute_stmt_return(f'''
                SELECT session_id, username, login_time, logout_time FROM {T.LOGIN_HISTORY_TABLE.value}
                ORDER BY session_id DESC
            ''')
        return [
            LoginHistoryRecord(
                session_id=int(row[0]),
                username=str(row[1]) if row[1] is not None else "",
                login_time=str(row[2]) if len(row) > 2 and row[2] is not None else "",
                logout_time=str(row[3]) if len(row) > 3 and row[3] is not None else None
            )
            for row in rows if len(row) >= 4
        ]

    def clear_history(self) -> None:
        """Clear the login/logout history table."""
        execute_stmt(f'DELETE FROM {T.LOGIN_HISTORY_TABLE.value}')
        print("Login history cleared.")

    def get_login_history_as_list(self) -> List[List[str]]:
        """Get the login history as a list of lists for easy display."""
        history = self.get_all_history()
        return [[
            str(record.session_id),
            record.username,
            record.login_time,
            record.logout_time if record.logout_time else ""
        ] for record in history]