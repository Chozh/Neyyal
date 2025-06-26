from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QPushButton, QWidget, QSizePolicy
)
from configuration import COMPANY_NAME, COMPANY_ADDRESS, BANK_NAME, ACCOUNT_NO, IFSC_CODE
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

        # Bank details
        bank_layout = QVBoxLayout()
        bank_layout.addWidget(QLabel("<b>Bank Details:</b>"))
        bank_layout.addWidget(QLabel("Bank Name: " + BANK_NAME))
        bank_layout.addWidget(QLabel("Account No: " + ACCOUNT_NO))
        bank_layout.addWidget(QLabel("IFSC Code: " + IFSC_CODE))
        main_layout.addLayout(bank_layout)

        # Terms and conditions
        terms_layout = QVBoxLayout()
        terms_layout.addWidget(QLabel("<b>Terms and conditions:</b>"))
        self.terms_label = QLabel("Payment is due within 30 days.")
        terms_layout.addWidget(self.terms_label)
        main_layout.addLayout(terms_layout)

        # Authorised Signatory
        signatory_layout = QHBoxLayout()
        signatory_layout.addStretch()
        signatory_layout.addWidget(QLabel("Authorised Signatory"))
        main_layout.addLayout(signatory_layout)

        # Action buttons
        button_layout = QHBoxLayout()
        self.print_button = QPushButton("Print")
        self.export_button = QPushButton("Export As PDF")
        self.close_button = QPushButton("Close")
        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)

    def render_as_html(self) -> str:
        """
        Render the invoice report as an HTML string, including styles and a table for items.
        """
        invoice_info: Dict[str, Any] = getattr(self, "invoice_info", {})
        # Header info
        company_html = f"""
        <div style="font-family:Segoe UI,Arial,sans-serif;">
            <h2 style="margin-bottom:0;">{COMPANY_NAME}</h2>
            <div style="margin-bottom:16px;">{COMPANY_ADDRESS}</div>
        """

        # Invoice info
        company_html += f"""
            <div>
                <b>Invoice No:</b> {invoice_info.get('invoice_no', '')} &nbsp;&nbsp;
                <b>Date:</b> {invoice_info.get('invoice_date', '')} &nbsp;&nbsp;
                <b>Customer:</b> {invoice_info.get('customer_name', '')}
            </div>
        """

        # Amounts
        company_html += f"""
            <div style="margin-top:8px;">
                <b>Total Amount:</b> {invoice_info.get('total_amount', '')} &nbsp;&nbsp;
                <b>CGST:</b> {invoice_info.get('cgst', '')} &nbsp;&nbsp;
                <b>SGST:</b> {invoice_info.get('sgst', '')} &nbsp;&nbsp;
                <b>IGST:</b> {invoice_info.get('igst', '')} &nbsp;&nbsp;
                <b>Status:</b> {invoice_info.get('status', '')}
            </div>
        """

        # Table for items (if available)
        items = invoice_info.get('items', [])
        table_html = """
            <table border="1" cellspacing="0" cellpadding="4" style="margin-top:16px;width:100%;border-collapse:collapse;">
                <tr style="background:#f0f0f0;">
                    <th>Product</th>
                    <th>HSN No</th>
                    <th>QTY</th>
                    <th>Rate</th>
                    <th>Amount</th>
                </tr>
        """
        for item in items:
            table_html += f"""
                <tr>
                    <td>{item.get('description', '')}</td>
                    <td>{item.get('hsn', '')}</td>
                    <td>{item.get('quantity', '')}</td>
                    <td>{item.get('rate', '')}</td>
                    <td>{item.get('amount', '')}</td>
                </tr>
            """
        table_html += "</table>"

        # Footer (optional)
        company_html += table_html
        company_html += "</div>"

        return company_html

