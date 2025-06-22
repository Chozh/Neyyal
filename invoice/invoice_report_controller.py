from PyQt6.QtWidgets import QWidget, QMessageBox
from typing import Dict, Any, Optional
from .invoice_report_view import InvoiceReportDialog
from PyQt6.QtWidgets import QFileDialog
from xhtml2pdf import pisa  # type: ignore
class InvoiceViewController():
    """
    Controller for the InvoiceDialog.
    Handles showing the invoice report.
    """
    def __init__(self, parent: QWidget | None ):
        self.view = InvoiceReportDialog(invoice_info=None, parent=parent)
        self.setup_connections()

    def setup_connections(self):
        """Setup connections for the invoice report dialog."""
        # Connect close button to close the dialog
        self.view.close_button.clicked.connect(self.view.close)  # type: ignore
        # Connect print button to print the invoice report
        self.view.print_button.clicked.connect(self.print_invoice_report)  # type: ignore
        # Connect Export As PDF button to export the invoice report
        self.view.export_button.clicked.connect(self.export_invoice_report)  # type: ignore

    def show_invoice_report(self, invoice_info: Optional[Dict[str, Any]] = None):
        self.view = InvoiceReportDialog(invoice_info=invoice_info, parent=self.view)
        self.view.exec()

    def show(self):
        self.view.exec()
    
    def print_invoice_report(self) -> None:
        """
        Handle printing the invoice report.
        This is a placeholder for actual print logic.
        """
        QMessageBox.information(self.view, "Print", "Printing invoice report... (not implemented)")

    def export_invoice_report(self) -> None:
        """
        Export the invoice report as a PDF using reportlab and beautifulsoup4.
        """
        # Ask user where to save the PDF
        file_path, _ = QFileDialog.getSaveFileName(
            self.view, "Export Invoice as PDF", "", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        # Get the HTML content from the report view
        html_content = self.view.render_as_html()
        try:
            with open(file_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)  # type: ignore
            if pisa_status.err:  # type: ignore
                QMessageBox.critical(self.view, "Export Failed", "Failed to export PDF: HTML rendering error.")
            else:
                QMessageBox.information(self.view, "Export Successful", f"Invoice exported as PDF to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self.view, "Export Failed", f"Failed to export PDF: {e}")

