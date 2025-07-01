from typing import Optional
from PyQt6.QtWidgets import QWidget
from .tableview_model import TableViewModel
from .tableview_view import TableViewWidget
from .tableeditor_controller import TableEditorController

from typing import List, Any

class TableViewController:
    def __init__(self, table_name: str, parent: Optional[QWidget] = None):
        self.table_name = table_name
        self.parent = parent
        self.model = TableViewModel(self.table_name)
        self.headers: List[str]
        self.data: List[List[Any]]
        self.headers, self.data = self.model.get_headers_and_data()  # type: ignore

        # Create the main widget that contains the table and buttons
        self.view = TableViewWidget(self.table_name, self.headers, self.data, parent=self.parent)
        self.editor = TableEditorController(self.table_name, parent=self.view)
        self.setup_connections()

    def setup_connections(self):
        # Connect button actions to methods (implement as needed)
        self.view.add_btn.clicked.connect(self.add_entry)  # type: ignore
        self.view.update_btn.clicked.connect(self.update_entry)  # type: ignore
        self.view.delete_btn.clicked.connect(self.delete_entry)  # type: ignore
        self.view.view_btn.clicked.connect(self.view_entry)  # type: ignore
        self.view.close_btn.clicked.connect(self.close)  # type: ignore

    def add_entry(self):
        # Logic to add a new entry (show input fields, collect data, insert into DB, refresh table)
        self.editor.show_input_fields("ADD", self.table_name, [])

    def update_entry(self):
        # Logic to update the selected entry (get checked row, update in DB, refresh table)
        checked_row = self.view.model.get_checked_row()
        if checked_row:
            self.editor.show_input_fields("UPDATE", self.table_name, [str(val) for val in checked_row])

    def delete_entry(self):
        # Logic to delete the selected entry (get checked row, delete from DB, refresh table)
        checked_row = self.view.model.get_checked_row()
        if checked_row:
            if self.model.delete_entry(checked_row):
                self.model.refresh_data()

    def view_entry(self):
        # Logic to view the selected entry (get checked row, show in fields)
        checked_row = self.view.model.get_checked_row()
        if checked_row:
            self.editor.show_input_fields("VIEW", self.table_name, [str(val) for val in checked_row])

    def close(self):
        self.view.close()

    def set_data(self, data: list[list[Any]]):
        """Set new data for the table view."""
        self.data = data
        # Ensure headers is a list of str (no None values)
        safe_headers = [h if h != "" else "" for h in self.headers]
        self.view.set_data(safe_headers, self.data)