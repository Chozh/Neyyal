from typing import Optional
from PyQt6.QtWidgets import QWidget
from .tableview_model import fetch_table_data
from .tableview_view import TableViewEditorDialog

class TableViewController:
    def __init__(self, table_name: str, parent: Optional[QWidget] = None):
        self.table_name = table_name
        self.parent = parent
        self.headers, self.data = fetch_table_data(self.table_name)
        # Ensure headers is a list of str, replacing None with empty string or a placeholder
        self.headers = [h if h is not None else "" for h in self.headers]
        self.view = TableViewEditorDialog(self.table_name, self.headers, self.data, parent=self.parent)
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
        self.view.show_input_fields()
        # Implement DB insert and refresh logic as needed

    def update_entry(self):
        # Logic to update the selected entry (get checked row, update in DB, refresh table)
        checked_row = self.view.model.get_checked_row()
        if checked_row:
            self.view.show_input_fields([str(val) for val in checked_row])
            # Implement DB update and refresh logic as needed

    def delete_entry(self):
        # Logic to delete the selected entry (get checked row, delete from DB, refresh table)
        checked_row = self.view.model.get_checked_row()
        if checked_row:
            # Implement DB delete and refresh logic as needed
            pass

    def view_entry(self):
        # Logic to view the selected entry (get checked row, show in fields)
        checked_row = self.view.model.get_checked_row()
        if checked_row:
            self.view.show_input_fields([str(val) for val in checked_row])

    def exec(self):
        return self.view.exec()

    def close(self):
        self.view.close()

    def show(self):
        self.view.show()

    def get_model(self):
        return self.view.model

    def get_table_name(self) -> str:
        return self.table_name