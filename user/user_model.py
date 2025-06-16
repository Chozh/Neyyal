# user_model.py
from utils.DB_conn import execute_stmt, execute_stmt_return
from utils.Tables import TableName as T

class UserModel:
    def register_admin(self, name: str, username: str, phone: str, address: str, password: str) -> bool:
        return execute_stmt(
            f"INSERT INTO {T.USERS_TABLE} (name, username, phone, address, password) VALUES (?, ?, ?, ?, ?)",
            (name, username, phone, address, password)
        )

    def user_exists(self, username: str) -> bool:
        result = execute_stmt_return(f"SELECT 1 FROM {T.USERS_TABLE} WHERE username = ?", (username,))
        return bool(result)
    
