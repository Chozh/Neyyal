from enum import Enum

class TableName(Enum):
    USERS_TABLE = "users"
    LOGIN_HISTORY_TABLE = "login_history"
    ITEM_TABLE = "item"
    CATEGORY_TABLE = "category"
    SALES_ORDER_TABLE = "sales_orders"
    PURCHASE_ORDER_TABLE = "purchase_orders"
    SALES_PAYMENT_TABLE = "sales_payments"
    PURCHASE_PAYMENT_TABLE = "purchase_payments"
    INVOICE_TABLE = "invoice"
    CUSTOMER_TABLE = "customer"
    SHIFT_TABLE = "shift"
    LOOM_TABLE = "loom"
    SUPPLIER_TABLE = "supplier"
    STOCK_TABLE = "stock"
    EMPLOYEE_TABLE = "employee"
    PRODUCTION_TABLE = "production"
    PAYMENTS_TABLE = "payments"

def get_tables() -> list[str]:
    return [table.value for table in TableName]