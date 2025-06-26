from typing import Optional, Dict, Any
from utils.DB_conn import execute_stmt, execute_stmt_return_one
from utils.Tables import TableName as T

class InvoiceModel:
    """
    Model for interacting with the Invoice table.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_invoice_info(invoice_id: int) -> Optional[Dict[str, Any]]:
        row = execute_stmt_return_one(
            f"""SELECT invoice_id, sales_order_id, invoice_date, bill_to_name,
                    total_amount, cgst, sgst, igst, status
                FROM {T.INVOICE_TABLE.value} WHERE invoice_id = ?""",
            (invoice_id,)
        )
        if row and row[0]:
            return {
                "invoice_id": row[0],
                "sales_order_id": row[1],
                "invoice_date": row[2],
                "customer_name": row[3],
                "total_amount": row[4],
                "cgst": row[5],
                "sgst": row[6],
                "igst": row[7],
                "status": row[8],
            }
        return None

    @staticmethod
    def save_invoice(data: Dict[str, Any]) -> str:
        stmt = f"""
            INSERT INTO {T.INVOICE_TABLE.value} (
                sales_order_id, customer_id, invoice_date, payment_method, amount_due, amount_paid
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            data["sales_order_id"],
            data["customer_id"],
            data["invoice_date"],
            data.get("payment_method", ""),
            data.get("amount_due", 0),
            data.get("amount_paid", 0)
        )
        success = execute_stmt(stmt, params)
        if not success:
            return "-1"
        row = execute_stmt_return_one("SELECT last_insert_rowid()", ())
        if row and row[0]:
            return str(row[0])
        return "-1"

    @staticmethod
    def update_invoice(invoice_id: int, data: Dict[str, Any]) -> bool:
        stmt = f"""
            UPDATE {T.INVOICE_TABLE.value} SET
                sales_order_id = ?, customer_id = ?, invoice_date = ?, payment_method = ?, amount_due = ?, amount_paid = ?
            WHERE invoice_id = ?
        """
        params = (
            data["sales_order_id"],
            data["customer_id"],
            data["invoice_date"],
            data.get("payment_method", ""),
            data.get("amount_due", 0),
            data.get("amount_paid", 0),
            invoice_id
        )
        return execute_stmt(stmt, params)