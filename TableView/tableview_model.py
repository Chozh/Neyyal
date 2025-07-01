import logging
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import Any, List
from sqlalchemy import text
from utils.Tables import TableSchemaORM
from sqlalchemy.orm import declarative_base
from utils.DB_conn import engine, SessionLocal

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

Base = declarative_base()
class TableViewModel(GenericTableModel):
    """Model for displaying table data in a QTableView."""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.schema_orm = TableSchemaORM(name=self.table_name, type="table")
        headers, data = self.fetch_table_data(table_name)
        headers = [h if h != "" else "" for h in headers]
        super().__init__(headers, data) 
        Base.metadata.create_all(engine)

    def fetch_table_data(self, table_name: str) -> tuple[list[str], list[list[Any]]]:
        pragma_result = self.schema_orm.get_table_schema_orm(table_name)
        headers = [col.name for col in pragma_result["columns"]] if pragma_result else []
        with SessionLocal() as session:
            result = session.execute(text(f"SELECT * FROM {table_name}"))
            data = result.fetchall()
        return headers, [list(row) for row in data]
    
    def get_headers_and_data(self) -> tuple[list[str], list[list[Any]]]:
        """Returns the headers and data for the table."""
        return self.headers, self._data
    
    def refresh_data(self):
        """Refresh the data from the database."""
        headers, data = self.fetch_table_data(self.table_name)
        self.headers = headers
        self._data = data
        self.layoutChanged.emit()

    def delete_entry(self, rowdata: List[Any]) -> bool:
        """Delete an entry from the table based on primary key value."""
        pri_key: str
        col_num: int
        pri_key, col_num = self.schema_orm.get_primary_key_col_num(table_name=self.table_name)
        with SessionLocal() as session:
            try:
                session.delete(session.query(Base).filter(getattr(Base, pri_key) == rowdata[col_num]).first())
                session.commit()
                return True
            except Exception as e:
                logging.error(f"DataBase Error: Error deleting entry: {e} on table {self.table_name} with rowdata {rowdata}")
                session.rollback()
                return False

