from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateEdit,
    QTextEdit, QTableWidget, QPushButton, QWidget, QMessageBox,
    QListWidget, QListWidgetItem, QSizePolicy, QCheckBox
)
from PyQt6.QtCore import QDate, Qt
from typing import TypedDict
from .customer_model import CustomerModel

class PartySectionDict(TypedDict):
    layout: QVBoxLayout
    name: QLineEdit
    address: QTextEdit
    gstin: QLineEdit
    state: QLineEdit
    state_code: QLineEdit

class InvoiceDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Tax Invoice")
        self.setGeometry(100, 100, 1080, 768)

        # Invoice layout
        invoice_layout = QVBoxLayout(self)
        self.setLayout(invoice_layout)
        header_label = QLabel("<h1>Invoice Details</h1>")
        invoice_layout.addWidget(header_label)
        invoice_layout.addWidget(QLabel("<hr>"))

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # Set margins for the main layout
        main_layout.setSpacing(10)  # Set spacing between widgets
        # Header section
        header_layout = QHBoxLayout()
        header_left = QVBoxLayout()
        self.order_number_edit = QLineEdit()
        header_left.addWidget(self._create_label_input("Order Number:", self.order_number_edit))
        header_layout.addLayout(header_left, stretch=1)  # Set stretch factor to 1

        header_right = QVBoxLayout()
        self.invoice_date_edit = QDateEdit()
        self.invoice_date_edit.setCalendarPopup(True)
        self.invoice_date_edit.setDate(QDate.currentDate())
        self.invoice_date_edit.setDisplayFormat("dd/MM/yyyy")
        header_right.addWidget(self._create_label_input("Invoice Date:", self.invoice_date_edit))
        header_layout.addLayout(header_right, stretch=1)  # Set stretch factor to 1

        main_layout.addLayout(header_layout)

        main_layout.addWidget(QLabel("<hr>"))

        # Other details
        other_details_layout = QHBoxLayout()
        other_details_left = QVBoxLayout()
        self.transport_mode_edit = QLineEdit()
        self.vehicle_number_edit = QLineEdit()
        other_details_left.addWidget(self._create_label_input("Transportation Mode:", self.transport_mode_edit))
        other_details_left.addWidget(self._create_label_input("Vehicle Number:", self.vehicle_number_edit))
        other_details_layout.addLayout(other_details_left)
        other_details_right = QVBoxLayout()
        self.date_of_supply_edit = QLineEdit()
        self.place_of_supply_edit = QLineEdit()
        other_details_right.addWidget(self._create_label_input("Date of Supply:", self.date_of_supply_edit))
        other_details_right.addWidget(self._create_label_input("Place of Supply:", self.place_of_supply_edit))
        other_details_layout.addLayout(other_details_right)
        main_layout.addLayout(other_details_layout)
        main_layout.addWidget(QLabel("<hr>"))

        # Bill to Party and Ship to Party
        phead_layout = QHBoxLayout()
        phead_layout.addWidget(QLabel("<h2>Bill to Party</h2>"), stretch=2)  # Set stretch factor for Bill to Party
        phead_layout.addWidget(QLabel("<h2>Ship to Party</h2>"), stretch=1)  # Set stretch factor for Ship to Party
        fill_ship_to_party_checkbox = QCheckBox("Same as Bill to Party", self)
        fill_ship_to_party_checkbox.setChecked(True)  # Default checked
        phead_layout.addWidget(fill_ship_to_party_checkbox)  # Checkbox for filling ship to party
        phead_layout.addStretch()  # Add stretch to fill space
        main_layout.addLayout(phead_layout)
        party_layout = QHBoxLayout()
        self.bill_to_party = self._create_party_section()
        self.ship_to_party = self._create_party_section()
        party_layout.addLayout(self.bill_to_party['layout'])
        party_layout.addLayout(self.ship_to_party['layout'])
        main_layout.addLayout(party_layout)

        # --- Customer autocomplete setup ---
        self.customer_suggestions = QListWidget()
        self.customer_suggestions.setWindowFlags(Qt.WindowType.Popup)
        self.customer_suggestions.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.customer_suggestions.setFocusProxy(self.bill_to_party['name'])
        self.customer_suggestions.hide()
        self.customer_suggestions.itemClicked.connect(self._select_customer_suggestion)  # type: ignore
        self.bill_to_party['name'].textEdited.connect(self._show_customer_suggestions)  # type: ignore
        self.bill_to_party['name'].editingFinished.connect(self.customer_suggestions.hide)  # type: ignore
        main_layout.addWidget(QLabel("<hr>"))

        # Table for product details
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels(["SNo", "NAME OF PRODUCT", "HSN No", "QTY", "RATE", "AMOUNT"])  # type: ignore
        self.product_table.setRowCount(5)  # Initial rows
        main_layout.addWidget(self.product_table)

        # Total section
        total_layout = QVBoxLayout()
        self.amount_in_words_edit = QLineEdit()
        total_layout.addWidget(self._create_label_input("Total Invoice Amount in words:", self.amount_in_words_edit))

        # Totals table
        self.totals_table = QTableWidget()
        self.totals_table.setRowCount(7)
        self.totals_table.setColumnCount(1)
        self.totals_table.setVerticalHeaderLabels([  # type: ignore
            "Less: Discount", "Total Amount Before Tax", "Add: CGST @", "Add: SGST @",
            "Add: IGST @", "Total Amount After Tax"
        ])  # type: ignore
        total_layout.addWidget(self.totals_table)

        main_layout.addLayout(total_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Add scroll area for invoice details
        scrollArea = QWidget()
        scrollArea.setMinimumSize(800, 600)  # Set minimum size for the scroll area
        scrollArea.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )  # Allow it to expand in both directions
        scrollArea.setLayout(main_layout)
        invoice_layout.addWidget(scrollArea)

    def _create_party_section(self) -> PartySectionDict:
        layout = QVBoxLayout()
        name = QLineEdit()
        address = QTextEdit()
        gstin = QLineEdit()
        state = QLineEdit()
        state_code = QLineEdit()
        layout.addWidget(self._create_label_input("Name:", name))
        layout.addWidget(self._create_label_input("Address:", address))
        layout.addWidget(self._create_label_input("GSTIN:", gstin))
        layout.addWidget(self._create_label_input("State:", state))
        layout.addWidget(self._create_label_input("State Code:", state_code))
        return {
            "layout": layout,
            "name": name,
            "address": address,
            "gstin": gstin,
            "state": state,
            "state_code": state_code
        }

    def _create_label_input(self, label_text: str, input_widget: QWidget) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(input_widget)
        return container

    def collect_invoice_data(self) -> dict[str, str]:
        item = self.totals_table.item(5, 0)
        amount_due = item.text() if item is not None else "0"
        return {
            "sales_order_id": self.order_number_edit.text(),
            "customer_id": self.bill_to_party['name'].property("customer_id") or "",
            "invoice_date": self.invoice_date_edit.date().toString("yyyy-MM-dd"),
            "payment_method": "",  # Add logic if you have a payment method field
            "amount_due": amount_due,
            "amount_paid": "0",  # Add logic if you have a paid amount field
            # ...other fields as needed...
        }

    def _show_customer_suggestions(self, text: str):
        if not text:
            self.customer_suggestions.hide()
            return

        # Fetch matching customers using CustomerModel
        customers = CustomerModel.search_customers_by_name(text, limit=4)
 

        if not customers:
            self.customer_suggestions.hide()
            return

        self.customer_suggestions.clear()
        for customer in customers:
            item = QListWidgetItem(f"{customer['name']} (ID: {customer['customer_id']})")
            item.setData(Qt.ItemDataRole.UserRole, customer['customer_id'])
            self.customer_suggestions.addItem(item)

        # Position the suggestion list below the name edit
        pos = self.bill_to_party['name'].mapToGlobal(self.bill_to_party['name'].rect().bottomLeft())
        self.customer_suggestions.move(pos)
        self.customer_suggestions.resize(
            self.bill_to_party['name'].width(),
            self.customer_suggestions.sizeHintForRow(0) * min(4, len(customers))
        )
        self.customer_suggestions.show()
        self.customer_suggestions.raise_()

    def _select_customer_suggestion(self, item: QListWidgetItem):
        name_id_text = item.text()
        customer_id = item.data(Qt.ItemDataRole.UserRole)
        name = name_id_text.split(" (ID:")[0]
        self.bill_to_party['name'].setText(name)
        self.customer_suggestions.hide()
        # Fetch and fill other customer fields using customer_id
        customer_details = CustomerModel.get_customer_details(customer_id)
        if customer_details:
            self.bill_to_party['address'].setPlainText(customer_details['address'])
            self.bill_to_party['gstin'].setText(customer_details['gstin'])
            self.bill_to_party['state'].setText(customer_details['state'])
            self.bill_to_party['state_code'].setText(customer_details['state_code'])
        else:
            QMessageBox.warning(self, "Error", "Could not fetch customer details.")