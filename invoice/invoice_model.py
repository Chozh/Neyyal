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
        """
        Fetch invoice info as a dict for the report view.
        """
        row = execute_stmt_return_one(
            f"""SELECT invoice_id, invoice_date, bill_to_name, amount_in_words, 
                   state, state_code, total_amount, cgst, sgst, igst, status
                FROM {T.INVOICE_TABLE} WHERE invoice_id = ?""",
            (invoice_id,)
        )

        if row and len(row) >= 11 and row[0]:
            return {
                "invoice_no": row[0],
                "invoice_date": row[1],
                "customer_name": row[2],
                "amount_in_words": row[3],
                "state": row[4],
                "state_code": row[5],
                "total_amount": row[6],
                "cgst": row[7],
                "sgst": row[8],
                "igst": row[9],
                "status": row[10],
            }
        return None

    @staticmethod
    def save_invoice(data: Dict[str, Any]) -> str:
        """
        Insert a new invoice record and return the new invoice_id.
        """
        stmt = f"""
            INSERT INTO {T.INVOICE_TABLE} (
                invoice_date, reverse_charge, state, state_code,
                transport_mode, vehicle_number, date_of_supply, place_of_supply,
                bill_to_name, bill_to_address, bill_to_gstin, bill_to_state, bill_to_state_code,
                ship_to_name, ship_to_address, ship_to_gstin, ship_to_state, ship_to_state_code,
                amount_in_words, bank_name, account_no, ifsc_code, terms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data["invoice_date"],
            data["reverse_charge"],
            data["state"],
            data["state_code"],
            data["transport_mode"],
            data["vehicle_number"],
            data["date_of_supply"],
            data["place_of_supply"],
            data["bill_to_name"],
            data["bill_to_address"],
            data["bill_to_gstin"],
            data["bill_to_state"],
            data["bill_to_state_code"],
            data["ship_to_name"],
            data["ship_to_address"],
            data["ship_to_gstin"],
            data["ship_to_state"],
            data["ship_to_state_code"],
            data["amount_in_words"],
            data["bank_name"],
            data["account_no"],
            data["ifsc_code"],
            data["terms"]
        )
        # Use execute_stmt to insert, then fetch last rowid
        success = execute_stmt(stmt, params)
        if not success:
            return "-1"  # Indicate failure
        # If insert was successful, fetch the last inserted row ID 
        # Get last inserted invoice_id
        row = execute_stmt_return_one("SELECT last_insert_rowid()", ())
        if row and row[0]:
            return str(row[0])
        return "-1"  # Ensure a string is always returned
    

    @staticmethod
    def update_invoice(invoice_id: int, data: Dict[str, Any]) -> bool:
        """
        Update an existing invoice record.
        """
        stmt = f"""
            UPDATE {T.INVOICE_TABLE} SET
                invoice_date = ?, reverse_charge = ?, state = ?, state_code = ?,
                transport_mode = ?, vehicle_number = ?, date_of_supply = ?, place_of_supply = ?,
                bill_to_name = ?, bill_to_address = ?, bill_to_gstin = ?, bill_to_state = ?,
                bill_to_state_code = ?, ship_to_name = ?, ship_to_address = ?,
                ship_to_gstin = ?, ship_to_state = ?, ship_to_state_code = ?,
                amount_in_words = ?, bank_name = ?, account_no = ?, ifsc_code = ?, terms = ?
            WHERE invoice_id = ?
        """
        params = (
            data["invoice_date"],
            data["reverse_charge"],
            data["state"],
            data["state_code"],
            data["transport_mode"],
            data["vehicle_number"],
            data["date_of_supply"],
            data["place_of_supply"],
            data["bill_to_name"],
            data["bill_to_address"],
            data["bill_to_gstin"],
            data["bill_to_state"],
            data["bill_to_state_code"],
            data["ship_to_name"],
            data["ship_to_address"],
            data["ship_to_gstin"],
            data["ship_to_state"],
            data["ship_to_state_code"],
            data["amount_in_words"],
            data["bank_name"],
            data["account_no"],
            data["ifsc_code"],
            data["terms"],
            invoice_id
        )
        return execute_stmt(stmt, params)