from PyQt6.QtWidgets import QWidget, QMessageBox
from typing import Dict, Any, Optional
from .invoice_view import InvoiceDialog
from .invoice_model import InvoiceModel
from .invoice_report_view import InvoiceReportDialog

class InvoiceViewController:
    """
    Controller for the InvoiceDialog.
    Handles showing the invoice report.
    """
    def __init__(self, parent: QWidget | None = None):
        self.view = InvoiceDialog(parent)
        self.setup_connections()

    def setup_connections(self):
        self.view.save_button.clicked.connect(self.save_invoice_only)  # type: ignore
        self.view.cancel_button.clicked.connect(self.view.close)  # type: ignore

    def show_invoice_report(self, invoice_info: Optional[Dict[str, Any]] = None):
        dialog = InvoiceReportDialog(invoice_info=invoice_info, parent=self.view)
        dialog.exec()

    def save_invoice_only(self):
        invoice_data = self.view.collect_invoice_data()
        invoice_id = InvoiceModel.save_invoice(invoice_data)
        if invoice_id:
            QMessageBox.information(self.view, "Success", "Invoice saved successfully.")
        else:
            QMessageBox.warning(self.view, "Error", "Could not save invoice.")

    def show(self):
        self.view.exec()