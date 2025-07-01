# File: TableView/tableeditor_controller.py
from PyQt6.QtWidgets import QWidget
from typing import Optional
from .tableeditor_model import TableEditorModel
from .tableeditor_view import TableEditorView
class TableEditorController:
    def __init__(self, table_name: str, parent: Optional[QWidget] = None):
        self.model = TableEditorModel(table_name)
        self.columns = self.model.get_columns()
        self.view = TableEditorView(table_name, self.columns, parent)
        self.pk_col = self.columns[0] if self.columns else None  # Assumes first column is PK
        self.setup_connections()


    def setup_connections(self):
        self.view.add_btn.clicked.connect(self.add_row)  # type: ignore
        self.view.update_btn.clicked.connect(self.update_row)  # type: ignore
        self.view.cancel_btn.clicked.connect(self.view.close)  # type: ignore
        self.view.close_btn.clicked.connect(self.view.close)  # type: ignore

    def show_input_fields(self, OP: str, table: str, values: Optional[list[str]] = None):
        self.view.show_input_fields(values)
        if OP == "ADD":
            self.view.setWindowTitle(f"Add Entry to {self.model.table_name}")
        elif OP == "UPDATE":
            self.view.setWindowTitle(f"Update Entry in {self.model.table_name}")
        elif OP == "VIEW":
            self.view.setWindowTitle(f"View Entry in {self.model.table_name}")
        else:
            raise ValueError(f"Unknown operation: {OP}")
        
    def add_row(self):
        values = [field.text() for field in self.view.input_fields]
        if self.model.insert(tuple(values)):
            self.view.close()

    def update_row(self):
        values = [field.text() for field in self.view.input_fields]
        if self.pk_col and values:
            pk_value = values[0]
            if self.model.update(self.pk_col, pk_value, tuple(values)):
                self.view.close()