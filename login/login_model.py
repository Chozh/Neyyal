# model.py
# Model for user authentication (stub for demonstration)

from utils.DB_conn import execute_stmt, execute_stmt_return
from user.login_history import LoginHistory
from configuration import DB_PATH
from utils.Tables import TableName as T
from typing import Optional

class UserModel:
    def __init__(self):
        """Initialize the user model with DB_PATH and ensure guest user exists."""
        self.db_path = DB_PATH
        self.ensure_guest_user()

    def ensure_guest_user(self):
        """Ensure that the guest user exists in the database."""
        if not self.user_exists('guest'):
            self.add_user('guest', 'guest123')

    def user_exists(self, username: str) -> bool:
        """Check if a user exists in the database."""
        if not username:
            return False
        exists = execute_stmt_return(f"SELECT 1 FROM {T.USERS_TABLE} WHERE username = ?", (username,))
        return len(exists) > 0

    def validate_user(self, username: str, password: str) -> bool:
        """Validate user credentials."""
        row = execute_stmt_return(f"SELECT password FROM {T.USERS_TABLE} WHERE username = ?", (username,))
        if row and row[0][0] == password:
            LoginHistory().record_login(username)
            return True
        return False

    def add_user(self, username: str, password: str) -> None:
        """Add a new user to the model."""
        execute_stmt(f"INSERT OR IGNORE INTO {T.USERS_TABLE} (username, password) VALUES (?, ?)", (username, password))

    def remove_user(self, username: str) -> bool:
        """Remove a user from the model."""
        execute_stmt(f"DELETE FROM {T.USERS_TABLE} WHERE username = ?", (username,))
        return True

    def change_password(self, username: str, new_password: str) -> bool:
        """Change the password for a user."""
        execute_stmt(f"UPDATE {T.USERS_TABLE} SET password = ? WHERE username = ?", (new_password, username))
        return True

    def get_all_users(self) -> list[str]:
        """Get a list of all usernames."""
        rows = execute_stmt_return(f"SELECT username FROM {T.USERS_TABLE}")
        return [row[0] for row in rows]

    def get_user_password(self, username: str) -> Optional[str]:
        """Get the password for a user."""
        row = execute_stmt_return(f"SELECT password FROM {T.USERS_TABLE} WHERE username = ?", (username,))
        return row[0][0] if row else None

    def clear_users(self) -> bool:
        """Clear all users from the model."""
        execute_stmt(f"DELETE FROM {T.USERS_TABLE}")
        return True

    def load_users_from_db(self, db_path: str) -> bool:
        """Load users from a SQLite database."""
        rows = execute_stmt_return(f"SELECT username, password FROM {T.USERS_TABLE}")
        self.users = {row[0]: row[1] for row in rows}
        return True

    def save_users_to_db(self, db_path: str) -> bool:
        """Save users to a SQLite database."""
        if hasattr(self, "users"):
            for username, password in self.users.items():
                execute_stmt(f"INSERT OR REPLACE INTO {T.USERS_TABLE} (username, password) VALUES (?, ?)", (username, password))
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user with username and password."""
        if hasattr(self, "users") and username in self.users and self.users[username] == password:
            return True
        return False

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

    def get_user_last_login(self, username: str) -> str:
        """Get the last login time for a user."""
        history = LoginHistory().get_user_history(username)
        if history:
            return history[0][0]
        return ""

    def register_admin(self, name: str, username: str, phone: str, address: str, password: str) -> bool:
        """Register a new admin user."""
        return execute_stmt(
            f"INSERT INTO {T.USERS_TABLE} (name, username, phone, address, password) VALUES (?, ?, ?, ?, ?)",
            (name, username, phone, address, password)
        )
