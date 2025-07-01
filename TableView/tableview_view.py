from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QTableView, QPushButton,
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

    def get_checked_row(self) -> Optional[list[Any]]:
        for row in self.data_rows:
            if row[0]:
                return row[1:]  # Exclude checkbox state
        return None

class TableViewWidget(QWidget):
    def __init__(self, table_name: str, columns: list[str], data: list[list[Any]], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle(f"Table: {table_name}")
        self.resize(1000, 700)
        self.table_name = table_name
        self.columns = columns

        # Main vertical splitter for 4:1 layout
        splitter = QSplitter(Qt.Orientation.Vertical)
        self.top_widget = QWidget()
        self.bottom_widget = QWidget()
        splitter.addWidget(self.top_widget)
        splitter.addWidget(self.bottom_widget)
        splitter.setSizes([int(400), int(100)])  # type: ignore

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # --- Top widget: Table with scroll area ---
        self.input_layout = QHBoxLayout(self.top_widget)
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

        bottom_layout = QVBoxLayout()
        self.table_view = QTableView(self.bottom_widget)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # Create and set the model
        self.model = CheckBoxTableModel(data, columns, self)
        self.table_view.setModel(self.model)
        top_layout.addWidget(self.table_view)

        # --- Bottom widget: buttons ---
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

    def set_data(self, columns: list[str], data: list[list[Any]]) -> None:
        """Set new data for the table view."""
        self.columns = columns
        self.model.columns = [""] + columns  # Update checkbox column header
        self.model.data_rows = [[False] + row for row in data]  # Update checkbox state
        self.model.layoutChanged.emit()  # Notify the view to refresh

    def get_checked_row(self) -> Optional[list[Any]]:
        """Get the currently checked row data."""
        return self.model.get_checked_row()
    