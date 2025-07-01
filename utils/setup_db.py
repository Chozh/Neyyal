# setup_db.py

from utils.Tables import TableName as T
from utils.DB_conn import execute_stmt

class Setup_DB:
    def __init__(self):
        """Initialize the setup_db class and create necessary tables."""
        pass

    def create_tables(self):
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.POSITIONS_TABLE.value} (
                    position_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    position_name TEXT NOT NULL UNIQUE,
                    description TEXT
                )
        ''')
        print("Positions table created successfully.")
        
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.EMPLOYEE_TABLE.value} (
                    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    doj DATE NOT NULL DEFAULT (date('now')),
                    phone TEXT NOT NULL,
                    email TEXT,
                    address TEXT,
                    position_id NOT NULL,
                    salary REAL NOT NULL,
                    added_by INTEGER NOT NULL,
                    FOREIGN KEY (position_id) REFERENCES {T.POSITIONS_TABLE.value}(position_id)
                )
        ''')
        print("Employee table created successfully.")

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.USERS_TABLE.value} (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    user_type TEXT NOT NULL DEFAULT 'EMP',
                    added_by INTEGER NOT NULL,
                    employee_id INTEGER,
                    FOREIGN KEY (employee_id) REFERENCES {T.EMPLOYEE_TABLE.value}(employee_id)
                )
        ''')
        print("Users table created successfully.")

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.LOGIN_HISTORY_TABLE.value} (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    login_time TEXT,
                    logout_time TEXT,
                    FOREIGN KEY (username) REFERENCES {T.USERS_TABLE.value}(username)
                )
        ''')
        print("Login history table created successfully.")

        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.CATEGORY_TABLE.value} (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT NOT NULL UNIQUE
                )
        ''')
        print("Category table created successfully.")

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
        print("Item table created successfully.")


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
        print("Customer table created successfully.")

        execute_stmt(f'''
            CREATE TABLE IF NOT EXISTS {T.SALES_ORDER_TABLE.value} (
                sales_order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                FOREIGN KEY (customer_id) REFERENCES {T.CUSTOMER_TABLE.value}(customer_id)
            )
        ''')
        print("Sales order table created successfully.")

        execute_stmt(f'''
            CREATE TABLE IF NOT EXISTS {T.PURCHASE_ORDER_TABLE.value} (
                purchase_order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                FOREIGN KEY (supplier_id) REFERENCES {T.SUPPLIER_TABLE.value}(supplier_id)
            )
        ''')
        print("Purchase order table created successfully.")
        # --- SALES PAYMENTS ---
        execute_stmt(f'''
            CREATE TABLE IF NOT EXISTS {T.SALES_PAYMENT_TABLE.value} (
                sales_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sales_order_id INTEGER NOT NULL,
                payment_date TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT,
                FOREIGN KEY (sales_order_id) REFERENCES {T.SALES_ORDER_TABLE.value}(sales_order_id)
            )
        ''')
        print("Sales payment table created successfully.")
        # --- PURCHASE PAYMENTS ---
        execute_stmt(f'''
            CREATE TABLE IF NOT EXISTS {T.PURCHASE_PAYMENT_TABLE.value} (
                purchase_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_order_id INTEGER NOT NULL,
                payment_date TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT,
                FOREIGN KEY (purchase_order_id) REFERENCES {T.PURCHASE_ORDER_TABLE.value}(purchase_order_id)
            )
        ''')
        print("Purchase payment table created successfully.")
        # --- INVOICE TABLE ---
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.INVOICE_TABLE.value} (
                    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sales_order_id INTEGER NOT NULL,
                    customer_id INTEGER,
                    invoice_date TEXT NOT NULL,
                    payment_method TEXT,
                    amount_due REAL NOT NULL,
                    amount_paid REAL,
                    FOREIGN KEY (sales_order_id) REFERENCES {T.SALES_ORDER_TABLE.value}(sales_order_id),
                    FOREIGN KEY (customer_id) REFERENCES {T.CUSTOMER_TABLE.value}(customer_id)
                )
        ''')
        print("Invoice table created successfully.")
        # --- SHIFT TABLE ---
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.SHIFT_TABLE.value} (
                    shift_no INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL
                )
        ''')
        print("Shift table created successfully.")
        # --- LOOM TABLE ---
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.LOOM_TABLE.value} (
                    loom_id TEXT PRIMARY KEY,
                    loom_type TEXT NOT NULL,
                    loom_description TEXT,
                    item_id INTEGER NOT NULL,
                    FOREIGN KEY (item_id) REFERENCES {T.ITEM_TABLE.value}(item_id)
                )
        ''')
        print("Loom table created successfully.")
        # --- STOCK TABLE ---
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.STOCK_TABLE.value} (
                    stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (item_id) REFERENCES {T.ITEM_TABLE.value}(item_id)
                )
        ''')
        print("Stock table created successfully.")
        # --- SUPPLIER TABLE ---
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.SUPPLIER_TABLE.value} (
                    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    gstin TEXT
                )
        ''')
        print("Supplier table created successfully.")
        # --- PRODUCTION TABLE ---
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.PRODUCTION_TABLE.value} (
                    production_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    loom_id TEXT NOT NULL,
                    item_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    production_date TEXT NOT NULL,
                    shift_no INTEGER NOT NULL,
                    employee_id INTEGER NOT NULL,
                    FOREIGN KEY (employee_id) REFERENCES {T.EMPLOYEE_TABLE.value}(employee_id),
                    FOREIGN KEY (shift_no) REFERENCES {T.SHIFT_TABLE.value}(shift_no),
                    FOREIGN KEY (loom_id) REFERENCES {T.LOOM_TABLE.value}(loom_id),
                    FOREIGN KEY (item_id) REFERENCES {T.ITEM_TABLE.value}(item_id)
                )
        ''')
        print("Production table created successfully.")

        # --- PAYMENTS TABLE ---
        execute_stmt(f'''
                CREATE TABLE IF NOT EXISTS {T.PAYMENTS_TABLE.value} (
                    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sales_order_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    payment_date TEXT NOT NULL,
                    amount_paid REAL NOT NULL,
                    FOREIGN KEY (sales_order_id) REFERENCES {T.SALES_ORDER_TABLE.value}(sales_order_id),
                    FOREIGN KEY (customer_id) REFERENCES {T.CUSTOMER_TABLE.value}(customer_id)
                )
        ''')    

        print("All tables created successfully.")

    def drop_all_tables(self) -> None:
        """Drop all tables in the database."""
        for table in T:
            execute_stmt(f"DROP TABLE IF EXISTS {table.value}")
        print("All tables dropped successfully.")

    def add_sample_data(self) -> None:
        """Add sample data to the database tables."""
        # Add sample categories
        execute_stmt("INSERT INTO category (category_name) VALUES ('Cotton'), ('Ryan'), ('Nylan')")

        # Add sample items
        execute_stmt(
            "INSERT INTO item (item_name, category_id, item_description, price) VALUES "
            "('Cotton Yarn', 1, 'High quality cotton yarn', 100.0), "
            "('Ryan Yarn', 2, 'Premium Ryan yarn', 150.0), "
            "('Nylan Yarn', 3, 'Durable Nylan yarn', 200.0)"
        )
        # Add sample customers
        execute_stmt(
            "INSERT INTO customer (name, phone, email, address, gstin) VALUES "
            "('John Doe', '9876543210', 'aaa@mail.com', '123 Main St', '27AAAPL1234C1Z5'), "
            "('Jane Smith', '9876543211', 'bbb@mail.com', '456 Elm St', '27AAAPL1234C1Z6')"
        )
        # Add sample suppliers
        execute_stmt(
            "INSERT INTO supplier (name, phone, email, address, gstin) VALUES "
            "('Supplier One', '9876543212', 'sss@mail.com', '789 Oak St', '27AAAPL1234C1Z7')"
        )
        # Add sample positions
        execute_stmt(
            "INSERT INTO positions (position_name, description) VALUES "
            "('Manager', 'Oversees operations'), "
            "('Worker', 'Handles production tasks')"
        )
        # Add sample employees
        execute_stmt(
            "INSERT INTO employee (name, phone, email, address, position_id) VALUES "
            "('Alice', '9876543213', 'eee@mail.com', '321 Pine St', 1), "
            "('Bob', '9876543214', 'ooo@mail.com', '654 Maple St', 2)"
        )
        # Add sample stock
        execute_stmt(
            "INSERT INTO stock (item_id, quantity) VALUES "
            "(1, 100), (2, 200), (3, 300)"
        )
        # Add sample shifts
        execute_stmt(
            "INSERT INTO shift (shift_no, start_time, end_time) VALUES "
            "(1, '08:00:00', '16:00:00'), (2, '16:00:00', '00:00:00')"
        )
        # Add sample looms
        execute_stmt(
            "INSERT INTO loom (loom_id, loom_type, loom_description, item_id) VALUES "
            "('Loom1', 'Type A', 'Type A Loom', 1), ('Loom2', 'Type B', 'Type B Loom', 2)"
        )
        # Add sample production entries
        execute_stmt(
            "INSERT INTO production (loom_id, item_id, quantity, production_date, shift_no, employee_id) VALUES "
            "('Loom1', 1, 50, '2023-10-01', 1, 1), "
            "('Loom2', 2, 75, '2023-10-02', 2, 2)"
        )
        # Add sample sales orders
        execute_stmt(
            "INSERT INTO sales_orders (customer_id, order_date, total_amount) VALUES "
            "(1, '2023-10-01', 500.0), (2, '2023-10-02', 750.0)"
        )
        # Add sample purchase orders
        execute_stmt(
            "INSERT INTO purchase_orders (supplier_id, order_date, total_amount) VALUES "
            "(1, '2023-10-01', 300.0), (1, '2023-10-02', 450.0)"
        )
        # Add sample payments
        execute_stmt(
            "INSERT INTO payments (sales_order_id, customer_id, payment_date, amount_paid) VALUES "
            "(1, 1, '2023-10-01', 500.0), (2, 2, '2023-10-02', 750.0)"
        )
