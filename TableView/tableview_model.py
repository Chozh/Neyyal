from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import Any, List
from utils.DB_conn import execute_stmt_return

class GenericTableModel(QAbstractTableModel):
    def __init__(self, headers: List[str], data: List[List[Any]]):
        super().__init__()
        self.headers = headers
        self._data = data

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.headers)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
            else:
                return section + 1
        return None

def fetch_table_data(table_name: str) -> tuple[list[str | None], list[list[Any]]]:
    pragma_result = execute_stmt_return(f"PRAGMA table_info({table_name})")
    headers = [row[1] for row in pragma_result] if pragma_result else []
    data = execute_stmt_return(f"SELECT * FROM {table_name}")
    return headers, [list(row) for row in data]