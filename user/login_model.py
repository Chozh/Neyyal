# model.py
# Model for user authentication (stub for demonstration)

from utils.DB_conn import execute_stmt, execute_stmt_return
from configuration import DB_PATH
from utils.Tables import TableName as T
from typing import Optional

class UserModel:
    def __init__(self):
        """Initialize the user model with DB_PATH and ensure guest user exists."""
        self.db_path = DB_PATH

    def validate_user(self, username: str, password_hash: str) -> bool:
        """Validate user credentials. Returns user id if valid, else 0."""
        row = execute_stmt_return(
            f"SELECT password FROM {T.USERS_TABLE.value} WHERE username = ?", (username,)
        )
        if not row:
            return False
        stored_hash = row[0][0]  # Get the stored password hash
        if stored_hash == password_hash:
            return True
        return False

    def change_password(self, username: str, new_password: str) -> bool:
        """Change the password for a user."""
        execute_stmt(f"UPDATE {T.USERS_TABLE.value} SET password = ? WHERE username = ?", (new_password, username))
        return True

    def get_user_password(self, username: str) -> Optional[str]:
        """Get the password for a user."""
        row = execute_stmt_return(f"SELECT password FROM {T.USERS_TABLE.value} WHERE username = ?", (username,))
        return row[0][0] if row else None  # Return Password. None if user not found

    def get_user_type(self, username: str) -> Optional[str]:
        """Get the role of the user based on username."""
        row = execute_stmt_return(f"SELECT user_type FROM {T.USERS_TABLE.value} WHERE username = ?", (username,))
        return row[0][0] if row else None  # Default to '' if user not found

    def reset_password(self, username: str, new_password: str) -> bool:
        """Reset the password for a user."""
        result = execute_stmt(
            f"UPDATE {T.USERS_TABLE.value} SET password = ? WHERE username = ?", (new_password, username)
        )
        return result

    def is_username_valid(self, username: str) -> bool:
        """Check if the username is valid.""" 
        if not username or len(username) < 3 or len(username) > 20:
            return False
        if not username.isalnum():
            return False
        return True
    