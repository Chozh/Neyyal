from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableView, QPushButton, QLineEdit, QLabel,
    QWidget, QSplitter, QScrollArea, QAbstractItemView
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QObject
from typing import Optional, Any

class CheckBoxTableModel(QAbstractTableModel):
    def __init__(self, data: list[list[Any]], columns: list[str], parent: Optional[QObject] = None):
        super().__init__(parent)
        self.columns = [""] + columns  # Add checkbox column header
        self.data_rows = [[False] + row for row in data]  # Add checkbox state to each row

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.data_rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.columns)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return QVariant()
        row, col = index.row(), index.column()
        if col == 0:
            if role == Qt.ItemDataRole.CheckStateRole:
                return Qt.CheckState.Checked if self.data_rows[row][0] else Qt.CheckState.Unchecked
            if role == Qt.ItemDataRole.DisplayRole:
                return ""
        else:
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self.data_rows[row][col])
        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.EditRole):
        if not index.isValid():
            return False
        row, col = index.row(), index.column()
        if col == 0 and role == Qt.ItemDataRole.CheckStateRole:
            # Uncheck all other rows (single selection)
            for r in range(len(self.data_rows)):
                self.data_rows[r][0] = False
            self.data_rows[row][0] = (value == Qt.CheckState.Checked)
            self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount()-1, 0))
            return True
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        if index.column() == 0:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]
        return super().headerData(section, orientation, role)

    def get_checked_row(self):
        for row in self.data_rows:
            if row[0]:
                return row[1:]  # Exclude checkbox state
        return None

class TableViewEditorDialog(QDialog):
    def __init__(self, table_name: str, columns: list[str], data: list[list[Any]], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle(f"Table: {table_name}")
        self.resize(1000, 700)
        self.table_name = table_name
        self.columns = columns

        # Main vertical splitter for 1:4 layout
        splitter = QSplitter(Qt.Orientation.Vertical)
        self.top_widget = QWidget()
        self.bottom_widget = QWidget()
        splitter.addWidget(self.top_widget)
        splitter.addWidget(self.bottom_widget)
        splitter.setSizes([int(100), int(400)])  # type: ignore

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # --- Top widget: Entry/Edit fields ---
        self.input_layout = QHBoxLayout(self.top_widget)
        self.input_labels: list[QLabel] = []
        self.input_fields: list[QLineEdit] = []
        for col in columns:
            vbox = QVBoxLayout()
            label = QLabel(col, self.top_widget)
            field = QLineEdit(self.top_widget)
            vbox.addWidget(label)
            vbox.addWidget(field)
            self.input_labels.append(label)
            self.input_fields.append(field)
            self.input_layout.addLayout(vbox)
        self.hide_input_fields()

        top_scroll = QScrollArea(self.top_widget)
        top_inner = QWidget()
        top_inner.setLayout(self.input_layout)
        top_scroll.setWidget(top_inner)
        top_scroll.setWidgetResizable(True)
        top_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        top_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        top_layout = QVBoxLayout(self.top_widget)
        top_layout.addWidget(top_scroll)
        self.top_widget.setLayout(top_layout)

        # --- Bottom widget: Table and buttons with scroll area ---
        bottom_layout = QVBoxLayout()
        self.table_view = QTableView(self.bottom_widget)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # Create and set the model
        self.model = CheckBoxTableModel(data, columns, self)
        self.table_view.setModel(self.model)
        bottom_layout.addWidget(self.table_view)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Entry")
        self.update_btn = QPushButton("Update Entry")
        self.delete_btn = QPushButton("Delete Entry")
        self.view_btn = QPushButton("View Entry")
        self.close_btn = QPushButton("Close")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.view_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_btn)
        bottom_layout.addLayout(btn_layout)

        bottom_inner = QWidget()
        bottom_inner.setLayout(bottom_layout)
        bottom_scroll = QScrollArea(self.bottom_widget)
        bottom_scroll.setWidget(bottom_inner)
        bottom_scroll.setWidgetResizable(True)
        bottom_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        bottom_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        bottom_main_layout = QVBoxLayout(self.bottom_widget)
        bottom_main_layout.addWidget(bottom_scroll)
        self.bottom_widget.setLayout(bottom_main_layout)

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

    def hide_input_fields(self):
        for field in self.input_fields:
            field.hide()
        for label in self.input_labels:
            label.hide()

    def on_checkbox_changed(self):
        row_data = self.model.get_checked_row()
        if row_data:
            self.show_input_fields([str(val) for val in row_data])