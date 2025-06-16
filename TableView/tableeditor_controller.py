from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt6.QtWidgets import QWidget
from typing import Any, Optional, Sequence
from .tableeditor_model import TableEditorModel
from .tableeditor_view import TableEditorView

class TableEditorTableModel(QAbstractTableModel):
    def __init__(self, columns: list[str], data: Sequence[Sequence[Any]]):
        super().__init__()
        self.columns = columns
        self._data = data

    def get_row(self, row: int) -> list[str]:
        return [str(item) for item in self._data[row]]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.columns)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.columns[section]
            else:
                return section + 1
        return None

class TableEditorController:
    def __init__(self, table_name: str, parent: Optional[QWidget] = None):
        self.model = TableEditorModel(table_name)
        self.columns = self.model.get_columns()
        self.view = TableEditorView(table_name, self.columns, parent)
        self.pk_col = self.columns[0] if self.columns else None  # Assumes first column is PK
        self.setup_connections()
        self.refresh_table()

    def setup_connections(self):
        self.view.add_btn.clicked.connect(self.add_row)  # type: ignore
        self.view.update_btn.clicked.connect(self.update_row)  # type: ignore
        self.view.delete_btn.clicked.connect(self.delete_row)  # type: ignore
        self.view.refresh_btn.clicked.connect(self.refresh_table)  # type: ignore
        self.view.filter_btn.clicked.connect(self.filter_table)  # type: ignore
        self.view.sort_btn.clicked.connect(self.sort_table)  # type: ignore
        self.view.table_view.clicked.connect(self.on_row_selected)  # type: ignore

    def refresh_table(self) -> None:
        data = self.model.get_all()
        self.table_model = TableEditorTableModel(self.columns, data)
        self.view.table_view.setModel(self.table_model)
        self.view.hide_input_fields()

    def add_row(self) -> None:
        self.view.show_input_fields()
        # Use a modal dialog for input, or just read fields and insert
        values = tuple(field.text() for field in self.view.input_fields)
        if all(values) and self.model.insert(values):
            self.refresh_table()
            self.view.hide_input_fields()

    def update_row(self) -> None:
        index = self.view.table_view.currentIndex()
        if not index.isValid() or not self.pk_col:
            return
        row = index.row()
        pk_val = self.table_model.get_row(row)[0]
        self.view.show_input_fields(self.table_model.get_row(row))
        values = tuple(field.text() for field in self.view.input_fields)
        if all(values) and self.model.update(self.pk_col, pk_val, values):
            self.refresh_table()
            self.view.hide_input_fields()

    def delete_row(self) -> None:
        index = self.view.table_view.currentIndex()
        if not index.isValid() or not self.pk_col:
            return
        row = index.row()
        pk_val = self.table_model.get_row(row)[0]
        if self.model.delete(self.pk_col, pk_val):
            self.refresh_table()
            self.view.hide_input_fields()
        if self.model.delete(self.pk_col, pk_val):
            self.refresh_table()
            self.view.hide_input_fields()

    def filter_table(self) -> None:
        col = self.view.filter_col.currentText()
        val = self.view.filter_edit.text()
        data = self.model.filter(col, val)
        self.table_model = TableEditorTableModel(self.columns, data)
        self.view.table_view.setModel(self.table_model)

    def sort_table(self) -> None:
        col = self.view.sort_col.currentText()
        data = self.model.sort(col)
        self.table_model = TableEditorTableModel(self.columns, data)
        self.view.table_view.setModel(self.table_model)

    def on_row_selected(self, index: QModelIndex) -> None:
        row = index.row()
        self.view.show_input_fields(self.table_model.get_row(row))

    def exec(self):
        self.view.exec()