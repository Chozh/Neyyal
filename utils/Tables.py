from enum import Enum

class TableName(Enum):
    USERS_TABLE = "users"
    LOGIN_HISTORY_TABLE = "login_history"
    ITEM_TABLE = "item"
    CATEGORY_TABLE = "category"
    ORDER_TABLE = "orders"
    INVOICE_TABLE = "invoice"
    CUSTOMER_TABLE = "customer"
    SHIFT_TABLE = "shift"
    LOOM_TABLE = "loom"

 

def get_tables() -> list[str]:
    """Get a list of all table names."""
    return [table.value for table in TableName]