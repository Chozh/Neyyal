from typing import Optional, List, Dict, Any
from utils.DB_conn import execute_stmt_return, execute_stmt_return_one

class CustomerModel:
    @staticmethod
    def search_customers_by_name(name_prefix: str, limit: int = 4) -> List[Dict[str, Any]]:
        """
        Returns a list of dicts with customer_id and name for customers whose names start with the given prefix.
        """
        results = execute_stmt_return(
            "SELECT customer_id, name FROM customer WHERE name LIKE ? LIMIT ?",
            (f"{name_prefix}%", limit)
        )
        return [{"customer_id": row[0], "name": row[1]} for row in results]

    @staticmethod
    def get_customer_details(customer_id: int) -> Optional[Dict[str, Any]]:
        """
        Returns a dict with address, gstin, state, state_code for the given customer_id.
        """
        row = execute_stmt_return_one(
            "SELECT address, gstin, state, state_code FROM customer WHERE customer_id = ?",
            (customer_id,)
        )
        if row and len(row) == 4:
            return {
                "address": row[0] or "",
                "gstin": row[1] or "",
                "state": row[2] or "",
                "state_code": row[3] or ""
            }
        return None