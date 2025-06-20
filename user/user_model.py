# user_model.py
from utils.DB_conn import execute_stmt, execute_stmt_return
from utils.Tables import TableName as T
from utils.session import get_current_user_id

class UserModel:
    def register_admin(self, name: str, username: str, phone: str, address: str, password: str) -> bool:
        added_by = get_current_user_id()
        return execute_stmt(
            f"INSERT INTO {T.USERS_TABLE.value} (name, username, phone, address, password, user_type, added_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, username, phone, address, password, "ADMIN", added_by)
        )

    def register_employee(self, name: str, username: str, phone: str, address: str, password: str) -> bool:
        added_by = get_current_user_id()
        return execute_stmt(
            f"INSERT INTO {T.USERS_TABLE.value} (name, username, phone, address, password, user_type, added_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, username, phone, address, password, "EMP", added_by)
        )

    def user_exists(self, username: str) -> bool:
        result = execute_stmt_return(f"SELECT 1 FROM {T.USERS_TABLE.value} WHERE username = ?", (username,))
        return bool(result)

