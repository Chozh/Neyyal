# model.py
# Model for user authentication (stub for demonstration)

from utils.DB_conn import execute_stmt, execute_stmt_return
from configuration import DB_PATH
from utils.Tables import TableName as T
from typing import Optional
import hashlib

class UserModel:
    def __init__(self):
        """Initialize the user model with DB_PATH and ensure guest user exists."""
        self.db_path = DB_PATH

    def user_exists(self, username: str) -> bool:
        """Check if a user exists in the database."""
        if not username:
            return False
        exists = execute_stmt_return(f"SELECT 1 FROM {T.USERS_TABLE.value} WHERE username = ?", (username,))
        return len(exists) > 0

    def validate_user(self, username: str, password: str) -> int:
        """Validate user credentials. Returns user id if valid, else 0."""
        row = execute_stmt_return(
            f"SELECT id, password FROM {T.USERS_TABLE.value} WHERE username = ?", (username,)
        )
        if not row:
            return 0
        stored_hash = row[0][1]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if stored_hash == password_hash:
            return row[0][0]
        return 0

    def change_password(self, username: str, new_password: str) -> bool:
        """Change the password for a user."""
        execute_stmt(f"UPDATE {T.USERS_TABLE.value} SET password = ? WHERE username = ?", (new_password, username))
        return True

    def get_user_password(self, username: str) -> Optional[str]:
        """Get the password for a user."""
        row = execute_stmt_return(f"SELECT password FROM {T.USERS_TABLE.value} WHERE username = ?", (username,))
        return row[0][0] if row else None

    def save_users_to_db(self, db_path: str) -> bool:
        """Save users to a SQLite database."""
        if hasattr(self, "users"):
            for username, password in self.users.items():
                execute_stmt(f"INSERT OR REPLACE INTO {T.USERS_TABLE.value} (username, password) VALUES (?, ?)", (username, password))
        return True

    def get_user_role(self, username: str) -> str:
        """Get the role of the user based on username."""
        if username == 'admin':
            return 'admin'
        elif username.startswith('emp'):
            return 'employee'
        return 'guest'

    def reset_password(self, username: str, new_password: str) -> bool:
        """Reset the password for a user."""
        if hasattr(self, "users") and username in self.users:
            self.users[username] = new_password
            return True
        return False

    def is_password_strong(self, password: str) -> bool:
        """Check if the password meets strength criteria."""
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isalpha() for char in password):
            return False
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password):
            return False
        return True

    def change_username(self, old_username: str, new_username: str) -> bool:
        """Change the username of a user."""
        if hasattr(self, "users") and old_username in self.users and new_username not in self.users:
            self.users[new_username] = self.users.pop(old_username)
            return True
        return False

    def get_user_count(self) -> int:
        """Get the total number of users."""
        if hasattr(self, "users"):
            return len(self.users)
        return 0

    def is_username_valid(self, username: str) -> bool:
        """Check if the username is valid.""" 
        if not username or len(username) < 3 or len(username) > 20:
            return False
        if not username.isalnum():
            return False
        return True

    def get_user_type(self, username: str) -> str:
        """Get the user_type for a user."""
        row = execute_stmt_return(f"SELECT user_type FROM {T.USERS_TABLE.value} WHERE username = ?", (username,))
        return row[0][0] if row else "EMP"
