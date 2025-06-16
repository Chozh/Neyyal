from typing import Optional, Dict, Any

class InvoiceReportModel:
    """
    Model to interact with the Invoice table and fetch invoice details.
    Replace the mock implementation with actual DB queries as needed.
    """

    def __init__(self, db_conn: Any):
        self.db_conn = db_conn

    def get_invoice_by_no(self, invoice_no: str) -> Optional[Dict[str, Any]]:
        """
        Fetch invoice details by invoice number.
        Returns a dictionary with invoice info or None if not found.
        """
        # Example query, replace with your actual DB logic
        cursor = self.db_conn.cursor()
        cursor.execute(
            "SELECT invoice_no, invoice_date, customer_name, total_amount, cgst, sgst, igst, status "
            "FROM invoice WHERE invoice_no = ?", (invoice_no,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "invoice_no": row[0],
                "invoice_date": row[1],
                "customer_name": row[2],
                "total_amount": row[3],
                "cgst": row[4],
                "sgst": row[5],
                "igst": row[6],
                "status": row[7],
            }
        return None