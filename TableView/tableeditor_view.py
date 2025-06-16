from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableView, QPushButton, QLineEdit, QLabel, QComboBox, QWidget
)

class TableEditorView(QDialog):
    def __init__(self, table_name: str, columns: list[str], parent: 'QWidget | None' = None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Table: {table_name}")
        self.resize(900, 600)
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        self.table_view = QTableView(self)
        main_layout.addWidget(self.table_view)

        # Controls
        controls = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.refresh_btn = QPushButton("Refresh")
        controls.addWidget(self.add_btn)
        controls.addWidget(self.update_btn)
        controls.addWidget(self.delete_btn)
        controls.addWidget(self.refresh_btn)
        main_layout.addLayout(controls)

        # Filter and sort
        filter_sort = QHBoxLayout()
        self.filter_col = QComboBox()
        self.filter_col.addItems([str(col) for col in columns]) # type: ignore
        self.filter_edit = QLineEdit()
        self.filter_btn = QPushButton("Filter")
        self.sort_col = QComboBox()
        self.sort_col.addItems([str(col) for col in columns]) # type: ignore
        self.sort_btn = QPushButton("Sort")
        filter_sort.addWidget(QLabel("Filter by:"))
        filter_sort.addWidget(self.filter_col)
        filter_sort.addWidget(self.filter_edit)
        filter_sort.addWidget(self.filter_btn)
        filter_sort.addSpacing(20)
        filter_sort.addWidget(QLabel("Sort by:"))
        filter_sort.addWidget(self.sort_col)
        filter_sort.addWidget(self.sort_btn)
        main_layout.addLayout(filter_sort)

        # For add/update dialogs
        self.input_fields = [QLineEdit(self) for _ in columns]
        self.input_labels = [QLabel(col, self) for col in columns]
        self.input_layout = QHBoxLayout()
        for label, field in zip(self.input_labels, self.input_fields):
            vbox = QVBoxLayout()
            vbox.addWidget(label)
            vbox.addWidget(field)
            self.input_layout.addLayout(vbox)
        main_layout.addLayout(self.input_layout)
        self.hide_input_fields()
        self.hide_input_fields()

    def show_input_fields(self, values: list[str] | None = None):
        for field in self.input_fields:
            field.show()
        if values:
            for field, val in zip(self.input_fields, values):
                field.setText(str(val))
        else:
            for field in self.input_fields:
                field.clear()

    def hide_input_fields(self):
        for field in self.input_fields:
            field.hide()