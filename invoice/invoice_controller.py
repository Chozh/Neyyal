from PyQt6.QtWidgets import QWidget
from .invoice_view import InvoiceDialog
from .invoice_report_controller import InvoiceViewController
from .invoice_model import InvoiceModel
from typing import Optional

class InvoiceController:
    def __init__(self, parent: Optional[QWidget] = None):
        self.view = InvoiceDialog(parent)
        self.setup_connections()

    def setup_connections(self):
        """Setup connections for the invoice dialog."""
        # Connect Generate Invoice button to generate invoice
        self.view.generate_button.clicked.connect(self.generate_invoice)  # type: ignore
        # Connect Cancel Invoice button to close the dialog
        self.view.cancel_button.clicked.connect(self.view.reject)  # type: ignore

    def show_invoice_dialog(self):
        """Show the invoice dialog for creating a new invoice."""
        self.view.exec()

    def generate_invoice(self):
        invoice_data = self.view.collect_invoice_data()
        InvoiceModel.save_invoice(invoice_data)
        self.view_invoice()

    def view_invoice(self):
        # To show the invoice dialog:
        parent_widget = self.view.parent()
        if not isinstance(parent_widget, QWidget):
            parent_widget = None
        controller = InvoiceViewController(parent=parent_widget)
        controller.show()