from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateEdit,
    QTextEdit, QTableWidget, QPushButton, QWidget, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import QDate, Qt
from typing import TypedDict
from configuration import COMPANY_NAME, COMPANY_ADDRESS
from .invoice_report_view import InvoiceReportDialog
from .invoice_model import InvoiceModel
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
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Header section
        header_layout = QHBoxLayout()
        company_layout = QVBoxLayout()
        company_layout.addWidget(QLabel(f"<b>{COMPANY_NAME}</b>"))
        company_layout.addWidget(QLabel(COMPANY_ADDRESS))
        header_layout.addLayout(company_layout)

        # Invoice details
        invoice_layout = QVBoxLayout()
        self.invoice_date_edit = QDateEdit()
        self.invoice_date_edit.setCalendarPopup(True)
        self.invoice_date_edit.setDate(QDate.currentDate())
        invoice_layout.addWidget(self._create_label_input("Invoice Date:", self.invoice_date_edit))
        header_layout.addLayout(invoice_layout)

        main_layout.addLayout(header_layout)

        # Other details
        other_details_layout = QHBoxLayout()
        other_details_left = QVBoxLayout()
        self.reverse_charge_edit = QLineEdit()
        self.state_edit = QLineEdit()
        self.state_code_edit = QLineEdit()
        other_details_left.addWidget(self._create_label_input("Reverse Charge:", self.reverse_charge_edit))
        other_details_left.addWidget(self._create_label_input("State:", self.state_edit))
        other_details_left.addWidget(self._create_label_input("State Code:", self.state_code_edit))
        other_details_layout.addLayout(other_details_left)

        other_details_right = QVBoxLayout()
        self.transport_mode_edit = QLineEdit()
        self.vehicle_number_edit = QLineEdit()
        self.date_of_supply_edit = QLineEdit()
        self.place_of_supply_edit = QLineEdit()
        other_details_right.addWidget(self._create_label_input("Transportation Mode:", self.transport_mode_edit))
        other_details_right.addWidget(self._create_label_input("Vehicle Number:", self.vehicle_number_edit))
        other_details_right.addWidget(self._create_label_input("Date of Supply:", self.date_of_supply_edit))
        other_details_right.addWidget(self._create_label_input("Place of Supply:", self.place_of_supply_edit))
        other_details_layout.addLayout(other_details_right)

        main_layout.addLayout(other_details_layout)

        # Bill to Party and Ship to Party
        party_layout = QHBoxLayout()
        self.bill_to_party = self._create_party_section("Bill to Party")
        self.ship_to_party = self._create_party_section("Ship to Party")
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

        # Table for product details
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels(["Count", "NAME OF PRODUCT", "HSN No", "QTY", "RATE", "AMOUNT"])  # type: ignore
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
            "Add: IGST @", "Total Amount After Tax", "GST Payable on reverse Charge"
        ])  # type: ignore
        total_layout.addWidget(self.totals_table)

        main_layout.addLayout(total_layout)

        # Bank details
        bank_layout = QVBoxLayout()
        bank_layout.addWidget(QLabel("<b>Bank Details:</b>"))
        self.bank_name_edit = QLineEdit()
        self.account_no_edit = QLineEdit()
        self.ifsc_code_edit = QLineEdit()
        bank_layout.addWidget(self._create_label_input("Bank Name:", self.bank_name_edit))
        bank_layout.addWidget(self._create_label_input("Account No:", self.account_no_edit))
        bank_layout.addWidget(self._create_label_input("IFSC Code:", self.ifsc_code_edit))
        main_layout.addLayout(bank_layout)

        # Terms and conditions
        terms_layout = QVBoxLayout()
        terms_layout.addWidget(QLabel("<b>Terms and conditions:</b>"))
        self.terms_text = QTextEdit()
        terms_layout.addWidget(self.terms_text)
        main_layout.addLayout(terms_layout)

        # Authorised Signatory
        signatory_layout = QHBoxLayout()
        signatory_layout.addStretch()
        signatory_layout.addWidget(QLabel("Authorised Signatory"))
        main_layout.addLayout(signatory_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.print_button = QPushButton("Generate")
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Connect Print button to save and show InvoiceReportDialog
        self.print_button.clicked.connect(self.save_and_show_invoice_report)  # type: ignore

    def save_and_show_invoice_report(self):
        invoice_data = {
            "invoice_date": self.invoice_date_edit.date().toString("yyyy-MM-dd"),
            "reverse_charge": self.reverse_charge_edit.text(),
            "state": self.state_edit.text(),
            "state_code": self.state_code_edit.text(),
            "transport_mode": self.transport_mode_edit.text(),
            "vehicle_number": self.vehicle_number_edit.text(),
            "date_of_supply": self.date_of_supply_edit.text(),
            "place_of_supply": self.place_of_supply_edit.text(),
            "bill_to_name": self.bill_to_party['name'].text(),
            "bill_to_address": self.bill_to_party['address'].toPlainText(),
            "bill_to_gstin": self.bill_to_party['gstin'].text(),
            "bill_to_state": self.bill_to_party['state'].text(),
            "bill_to_state_code": self.bill_to_party['state_code'].text(),
            "ship_to_name": self.ship_to_party['name'].text(),
            "ship_to_address": self.ship_to_party['address'].toPlainText(),
            "ship_to_gstin": self.ship_to_party['gstin'].text(),
            "ship_to_state": self.ship_to_party['state'].text(),
            "ship_to_state_code": self.ship_to_party['state_code'].text(),
            "amount_in_words": self.amount_in_words_edit.text(),
            "bank_name": self.bank_name_edit.text(),
            "account_no": self.account_no_edit.text(),
            "ifsc_code": self.ifsc_code_edit.text(),
            "terms": self.terms_text.toPlainText()
        }
        invoice_id = InvoiceModel.save_invoice(invoice_data)
        if invoice_id:
            dialog = InvoiceReportDialog(invoice_info={"invoice_id": invoice_id}, parent=self)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "Could not save invoice.")

    def _create_party_section(self, title: str) -> PartySectionDict:
        layout = QVBoxLayout()
        name = QLineEdit()
        address = QTextEdit()
        gstin = QLineEdit()
        state = QLineEdit()
        state_code = QLineEdit()
        layout.addWidget(QLabel(f"<b>{title}</b>"))
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
        return {
            "invoice_date": self.invoice_date_edit.date().toString("yyyy-MM-dd"),
            "reverse_charge": self.reverse_charge_edit.text(),
            "state": self.state_edit.text(),
            "state_code": self.state_code_edit.text(),
            "transport_mode": self.transport_mode_edit.text(),
            "vehicle_number": self.vehicle_number_edit.text(),
            "date_of_supply": self.date_of_supply_edit.text(),
            "place_of_supply": self.place_of_supply_edit.text(),
            "bill_to_name": self.bill_to_party['name'].text(),
            "bill_to_address": self.bill_to_party['address'].toPlainText(),
            "bill_to_gstin": self.bill_to_party['gstin'].text(),
            "bill_to_state": self.bill_to_party['state'].text(),
            "bill_to_state_code": self.bill_to_party['state_code'].text(),
            "ship_to_name": self.ship_to_party['name'].text(),
            "ship_to_address": self.ship_to_party['address'].toPlainText(),
            "ship_to_gstin": self.ship_to_party['gstin'].text(),
            "ship_to_state": self.ship_to_party['state'].text(),
            "ship_to_state_code": self.ship_to_party['state_code'].text(),
            "amount_in_words": self.amount_in_words_edit.text(),
            "bank_name": self.bank_name_edit.text(),
            "account_no": self.account_no_edit.text(),
            "ifsc_code": self.ifsc_code_edit.text(),
            "terms": self.terms_text.toPlainText()
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