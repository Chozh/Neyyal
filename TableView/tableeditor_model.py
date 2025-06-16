from typing import Any, List, Tuple
from utils.DB_conn import execute_stmt, execute_stmt_return

class TableEditorModel:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def get_columns(self) -> List[str]:
        pragma = execute_stmt_return(f"PRAGMA table_info({self.table_name})")
        return [str(row[1]) for row in pragma if row[1] is not None]

    def get_all(self) -> List[Tuple[Any, ...]]:
        return execute_stmt_return(f"SELECT * FROM {self.table_name}")

    def insert(self, values: Tuple[Any, ...]) -> bool:
        cols = self.get_columns()
        placeholders = ','.join(['?'] * len(cols))
        stmt = f"INSERT INTO {self.table_name} ({', '.join(cols)}) VALUES ({placeholders})"
        return execute_stmt(stmt, values)

    def update(self, pk_col: str, pk_val: Any, values: Tuple[Any, ...]) -> bool:
        cols = self.get_columns()
        set_clause = ', '.join([f"{col}=?" for col in cols if col != pk_col])
        stmt = f"UPDATE {self.table_name} SET {set_clause} WHERE {pk_col}=?"
        # Remove pk_col from values and append pk_val at the end
        update_values = tuple(v for i, v in enumerate(values) if cols[i] != pk_col) + (pk_val,)
        return execute_stmt(stmt, update_values)

    def delete(self, pk_col: str, pk_val: Any) -> bool:
        stmt = f"DELETE FROM {self.table_name} WHERE {pk_col}=?"
        return execute_stmt(stmt, (pk_val,))

    def filter(self, filter_col: str, filter_val: Any) -> List[Tuple[Any, ...]]:
        stmt = f"SELECT * FROM {self.table_name} WHERE {filter_col} LIKE ?"
        return execute_stmt_return(stmt, (f"%{filter_val}%",))

    def sort(self, sort_col: str, descending: bool = False) -> List[Tuple[Any, ...]]:
        order = "DESC" if descending else "ASC"
        stmt = f"SELECT * FROM {self.table_name} ORDER BY {sort_col} {order}"
        return execute_stmt_return(stmt)