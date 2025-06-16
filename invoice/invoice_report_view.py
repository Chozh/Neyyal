from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QPushButton, QWidget, QSizePolicy
)
from configuration import COMPANY_NAME, COMPANY_ADDRESS
from typing import Any, Dict, Optional

class InvoiceReportDialog(QDialog):
    def __init__(self, invoice_info: Optional[Dict[str, Any]], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Invoice Report")
        self.setGeometry(150, 150, 900, 600)

        main_layout = QVBoxLayout(self)

        # Header
        header_layout = QHBoxLayout()
        company_layout = QVBoxLayout()
        company_layout.addWidget(QLabel(f"<b>{COMPANY_NAME}</b>"))
        company_layout.addWidget(QLabel(COMPANY_ADDRESS))
        header_layout.addLayout(company_layout)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Invoice Info as labels
        info_layout = QHBoxLayout()
        invoice_no = invoice_info.get('invoice_no', '') if invoice_info else ''
        invoice_date = invoice_info.get('invoice_date', '') if invoice_info else ''
        customer_name = invoice_info.get('customer_name', '') if invoice_info else ''
        info_layout.addWidget(QLabel(f"<b>Invoice No:</b> {invoice_no}"))
        info_layout.addWidget(QLabel(f"<b>Date:</b> {invoice_date}"))
        info_layout.addWidget(QLabel(f"<b>Customer:</b> {customer_name}"))
        info_layout.addStretch()
        main_layout.addLayout(info_layout)

        # Amounts as labels
        amount_layout = QHBoxLayout()
        total_amount = invoice_info.get('total_amount', '') if invoice_info else ''
        cgst = invoice_info.get('cgst', '') if invoice_info else ''
        sgst = invoice_info.get('sgst', '') if invoice_info else ''
        igst = invoice_info.get('igst', '') if invoice_info else ''
        status = invoice_info.get('status', '') if invoice_info else ''
        amount_layout.addWidget(QLabel(f"<b>Total Amount:</b> {total_amount}"))
        amount_layout.addWidget(QLabel(f"<b>CGST:</b> {cgst}"))
        amount_layout.addWidget(QLabel(f"<b>SGST:</b> {sgst}"))
        amount_layout.addWidget(QLabel(f"<b>IGST:</b> {igst}"))
        amount_layout.addWidget(QLabel(f"<b>Status:</b> {status}"))
        amount_layout.addStretch()
        main_layout.addLayout(amount_layout)

        # Table for invoice items (optional, can be filled from another model method)
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels([  # type: ignore
            "Product", "HSN No", "QTY", "Rate", "Amount"
        ])
        self.report_table.setRowCount(0)
        self.report_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.report_table)

        # Action buttons
        button_layout = QHBoxLayout()
        self.print_button = QPushButton("View Invoice")
        self.export_button = QPushButton("Export")
        self.close_button = QPushButton("Close")
        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)

        self.close_button.clicked.connect(self.close)  # type: ignore
