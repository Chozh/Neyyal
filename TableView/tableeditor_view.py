from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QWidget
)

class TableEditorView(QDialog):
    def __init__(self, table_name: str, columns: list[str], parent: 'QWidget | None' = None):
        super().__init__(parent)
        self.setWindowTitle(f"Table: {table_name}")
        self.resize(900, 600)
        main_layout = QVBoxLayout(self)

        # --- Entry/Edit fields ---
        self.input_layout = QHBoxLayout()
        self.input_labels: list[QLabel] = []
        self.input_fields: list[QLineEdit] = []
        for col in columns:
            hbox_layout = QHBoxLayout()
            label = QLabel(col, self)
            self.input_labels.append(label)
            field = QLineEdit(self)
            self.input_fields.append(field)
            hbox_layout.addWidget(label)
            hbox_layout.addWidget(field)
            self.input_layout.addLayout(hbox_layout)

        input_scroll = QWidget(self)
        input_scroll.setMinimumHeight(100)
        input_scroll.setMinimumWidth(800)
        input_scroll.setMaximumHeight(150)
        input_scroll.setMaximumWidth(800)
        input_scroll.setSizePolicy(
            input_scroll.sizePolicy().Policy.Expanding,
            input_scroll.sizePolicy().Policy.Fixed
        )
        input_scroll.setLayout(self.input_layout)
        main_layout.addWidget(input_scroll)
        # --- Buttons ---
        self.button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Entry", self)
        self.update_btn = QPushButton("Update Entry", self)
        self.close_btn = QPushButton("Close", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.button_layout.addWidget(self.add_btn)
        self.button_layout.addWidget(self.update_btn)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.close_btn)
        self.button_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(self.button_layout)
        self.setLayout(main_layout)

    def show_input_fields(self, values: list[str] | None = None):
        for field in self.input_fields:
            field.show()
        for label in self.input_labels:
            label.show()
        if values:
            for field, val in zip(self.input_fields, values):
                field.setText(str(val))
        else:
            for field in self.input_fields:
                field.clear()

    def get_input_values(self) -> list[str]:
        return [field.text() for field in self.input_fields]
    
    def clear_input_fields(self):
        for field in self.input_fields:
            field.clear()

    def set_input_fields_readonly(self, readonly: bool):
        for field in self.input_fields:
            field.setReadOnly(readonly)

    # Enable/Disable fields and buttons based on operation type
    def enble_disable_buttons(self, OP: str) -> None:
        if OP == "ADD":
            self.add_btn.setEnabled(True)
            self.update_btn.setEnabled(False)
            self.cancel_btn.setEnabled(True)
            self.close_btn.setEnabled(False)
            self.clear_input_fields()
            self.set_input_fields_readonly(False)
        elif OP == "UPDATE":
            self.add_btn.setEnabled(False)
            self.update_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)
            self.close_btn.setEnabled(False)
            self.set_input_fields_readonly(False)
        elif OP == "VIEW":
            self.add_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)
            self.close_btn.setEnabled(True)
            self.set_input_fields_readonly(True)
    