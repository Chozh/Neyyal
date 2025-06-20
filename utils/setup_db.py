# setup_db.py

from utils.Tables import TableName as T
from utils.DB_conn import execute_stmt

class Setup_DB:
    def __init__(self):
        """Initialize the setup_db class and create necessary tables."""
        pass

    def create_tables(self):
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.USERS_TABLE.value} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    phone TEXT NOT NULL,
                    address TEXT NOT NULL,
                    password TEXT NOT NULL,
                    user_type TEXT NOT NULL DEFAULT 'EMP',
                    added_by INTEGER NOT NULL
                )
        ''')

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.LOGIN_HISTORY_TABLE.value} (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    FOREIGN KEY (user_id) REFERENCES {T.USERS_TABLE.value}(id)
                    login_time TEXT,
                    logout_time TEXT
                )
        ''')

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.ITEM_TABLE.value} (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    item_description TEXT,
                    price REAL NOT NULL,
                    FOREIGN KEY (category_id) REFERENCES {T.CATEGORY_TABLE.value}(category_id)
                )
        ''')

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.CATEGORY_TABLE.value} (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT NOT NULL UNIQUE
                )
        ''')

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.CUSTOMER_TABLE.value} (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    gstin TEXT,
                    state TEXT,
                    state_code TEXT
                )
        ''')

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.INVOICE_TABLE.value} (
                    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    customer_id INTEGER,
                    invoice_date TEXT NOT NULL,
                    payment_method TEXT,
                    amount_due REAL NOT NULL,
                    amount_paid REAL,
                    FOREIGN KEY (order_id) REFERENCES "order"(order_id),
                    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
                )
        ''')

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.SHIFT_TABLE.value} (
                    shift_no INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL
                )
        ''')

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.LOOM_TABLE.value} (
                    loom_id TEXT PRIMARY KEY,
                    item_id INTEGER NOT NULL,
                    FOREIGN KEY (item_id) REFERENCES {T.ITEM_TABLE.value}(item_id)
                )
        ''')


def create_login_history_table() -> None:
    execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.LOGIN_HISTORY_TABLE.value} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    login_time TEXT,
                    logout_time TEXT
                )
    ''')


