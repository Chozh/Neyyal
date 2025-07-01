from enum import Enum
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base
from utils.DB_conn import engine
from typing import Any, Dict, List

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
    POSITIONS_TABLE = "positions"
    
    @classmethod
    def get_table_names(cls) -> list[str]:
        return [table.value for table in cls]
    

Base = declarative_base()


class TableSchemaORM():
    """A class to represent a column's schema information (for ORM-style usage)."""
    def __init__(
        self,
        name: str,
        type: str,
        notnull: int = 0,
        default: str | None = None,
        primary_key: int = 0,
        cid: int | None = None
    ):
        self.name = name
        self.type = type
        self.notnull = notnull
        self.default = default
        self.primary_key = primary_key
        self.cid = cid

    def get_table_schema_orm(self, table_name: str) -> Dict[str, Any]:
        """
        Get schema using SQLAlchemy ORM inspector.
        Returns a dictionary with columns and foreign key info.
        """
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)

        # Build column schema objects
        self.column_schemas = [
            TableSchemaORM(
                name=col['name'],
                type=str(col['type']),
                notnull=0 if col.get('nullable', True) else 1,
                default=col.get('default'),
                primary_key=1 if col.get('primary_key', False) else 0,
                cid=col.get('cid')
            )
            for col in columns
        ]

        # Build foreign key info
        self.fk_info: List[Dict[str, Any]] = [
            {
                "constrained_columns": fk['constrained_columns'],
                "referred_table": fk['referred_table'],
                "referred_columns": fk['referred_columns']
            }
            for fk in foreign_keys
        ]

        return {
            "columns": self.column_schemas,
            "foreign_keys": self.fk_info
        }
    
    def get_primary_key(self, table_name: str) -> str:
        """
        Get the primary key column name for a given table.
        Returns the primary key column name or an empty string if not found.
        """
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        for col in columns:
            if col.get('primary_key'):
                return col['name']
        return ""

    # Return primary key and column number
    def get_primary_key_col_num(self, table_name: str) -> tuple[str, int]:
        """
        Get the primary key column index for a given table.
        Returns the index of the primary key column or -1 if not found.
        """
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        for idx, col in enumerate(columns):
            if col.get('primary_key'):
                return col['name'], idx
        return "", -1