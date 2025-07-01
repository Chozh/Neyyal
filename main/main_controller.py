import sys
from PyQt6.QtWidgets import QApplication
from user.login_controller import LoginController
from TableView.tableview_controller import TableViewController
from .main_view import MainWindow
from invoice.invoice_controller import InvoiceController
from settings.settings_controller import SettingsController
from user.session import get_current_session_id
from utils.Tables import TableName as T
from user.login_history import LoginHistory


class MainController:
    def __init__(self, app: QApplication):
        self.app = app
        self.window = MainWindow()
        self.setup_menu_connections()
        self.settings_controller = SettingsController(self.app)
        self.settings_controller.apply_global_styles(app) # Apply global styles
        # self.settings_controller.load_settings()  # Load settings on startup

    def setup_menu_connections(self) -> None:
        # Menu actions
        self.window.exit_action.triggered.connect(self.app.quit)  # type: ignore

        # User management actions
        self.window.users_action.triggered.connect(lambda: self.show_table(T.USERS_TABLE.value))  # type: ignore
        self.window.employees_action.triggered.connect(lambda: self.show_table(T.EMPLOYEE_TABLE.value))  # type: ignore
        self.window.customers_action.triggered.connect(lambda: self.show_table(T.CUSTOMER_TABLE.value))  # type: ignore
        self.window.suppliers_action.triggered.connect(lambda: self.show_table(T.SUPPLIER_TABLE.value))  # type: ignore

        # Production actions
        self.window.shifts_action.triggered.connect(lambda: self.show_table(T.SHIFT_TABLE.value))  # type: ignore
        self.window.looms_action.triggered.connect(lambda: self.show_table(T.LOOM_TABLE.value))  # type: ignore
        self.window.add_work_entry_action.triggered.connect(lambda: self.show_table(T.PRODUCTION_TABLE.value))  # type: ignore

        # Invoice actions
        self.window.generate_invoice_action.triggered.connect(self.show_invoice_dialog)  # type: ignore
        self.window.payments_action.triggered.connect(lambda: self.show_table(T.PAYMENTS_TABLE.value))  # type: ignore
        self.window.sales_orders_action.triggered.connect(lambda: self.show_table(T.SALES_ORDER_TABLE.value))  # type: ignore
        self.window.purchase_orders_action.triggered.connect(lambda: self.show_table(T.PURCHASE_ORDER_TABLE.value))  # type: ignore

        #Inventory actions
        self.window.items_action.triggered.connect(lambda: self.show_table(T.ITEM_TABLE.value))  # type: ignore
        self.window.categories_action.triggered.connect(lambda: self.show_table(T.CATEGORY_TABLE.value))  # type: ignore
        self.window.stock_action.triggered.connect(lambda: self.show_table(T.STOCK_TABLE.value))  # type: ignore

        # History actions
        self.window.login_history_action.triggered.connect(self.get_login_history)  # type: ignore
        self.window.invoice_history_action.triggered.connect(lambda: self.show_table(T.INVOICE_TABLE.value))  # type: ignore

        # Report actions
        self.window.sales_report_action.triggered.connect(lambda: self.show_table(T.SALES_ORDER_TABLE.value))  # type: ignore
        self.window.purchase_report_action.triggered.connect(lambda: self.show_table(T.PURCHASE_ORDER_TABLE.value))  # type: ignore
        self.window.production_report_action.triggered.connect(lambda: self.show_table(T.PRODUCTION_TABLE.value))  # type: ignore


        # Toolbar actions
        self.window.settings_action.triggered.connect(self.show_settings_dialog)  # type: ignore
        self.window.logout_action.triggered.connect(self.handle_logout)  # type: ignore

    def show_login(self) -> None:
        """Show the login dialog and handle user login."""
        while True:
            login = LoginController(self.window)
            result = login.exec()
            if result == 0:
                # User cancelled login, exit app
                sys.exit(0)
            # Only break loop if user is logged in
            if get_current_session_id() != 0:
                break

    def handle_logout(self):
        """Handle user logout: update logout time, clear session, show login."""
        if get_current_session_id() != 0:
            LoginHistory.record_logout(session_id=get_current_session_id())
        self.window.hide()
        self.show_login()
        self.window.show()

    def get_login_history(self):
        """Retrieve and display the login history for the current user."""
        if not get_current_session_id() != 0:
            return
        history = LoginHistory().get_login_history_as_list()
        if not history:
            self.window.show_message("Info", "No login history found for this user.")
        else:
            # Show login history in a table view
            controller = TableViewController(T.LOGIN_HISTORY_TABLE.value)
            controller.set_data(history)
            self.window.set_content(controller.view)  # Set the table widget as the main content

    def show_table(self, table_name: str):
        # Prevent actions if not logged in
        if not get_current_session_id() != 0:
            return
        controller = TableViewController(table_name)
        self.window.set_content(controller.view)  # Set the table widget as the main content

    def show_invoice_dialog(self):
        if not get_current_session_id() != 0:
            return
        invoice_controller = InvoiceController(self.window)
        invoice_controller.show_invoice_dialog()

    def show_settings_dialog(self):
        if not get_current_session_id() != 0:
            return
        self.settings_controller.show_settings()

    def run(self):
        """Run the main application loop, ensuring logout time is updated on exit."""
        #self.show_login()
        from user.session import set_current_session
        set_current_session("admin", 1)  # For testing purposes, set a dummy session
        self.window.show()
        try:
            self.app.exec()
        finally:
            # On app exit, update logout time if user is logged in
            if get_current_session_id() != 0:
                LoginHistory.record_logout(get_current_session_id())
                sys.exit(0)  # Ensure app exits cleanly after logout