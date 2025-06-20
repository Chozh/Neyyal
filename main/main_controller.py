import sys
from PyQt6.QtWidgets import QApplication
from login.login_controller import LoginController
from TableView.tableview_controller import TableViewController
from .main_view import MainWindow
from invoice.invoice_controller import InvoiceController
from settings.settings_controller import SettingsController
from utils.session import get_current_user_id
from utils.Tables import TableName as T
from user.login_history import record_logout


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
        self.window.users_action.triggered.connect(lambda: self.show_table(T.USERS_TABLE.value))  # type: ignore
        self.window.login_history_action.triggered.connect(lambda: self.show_table(T.LOGIN_HISTORY_TABLE.value))  # type: ignore
        self.window.generate_invoice_action.triggered.connect(self.show_invoice_dialog)  # type: ignore

        # Toolbar actions
        self.window.settings_action.triggered.connect(self.show_settings_dialog)  # type: ignore
        self.window.logout_action.triggered.connect(self.login_controller_handle_logout)  # type: ignore

    def show_login(self) -> None:
        while True:
            login = LoginController(self.window)
            result = login.exec()
            if result == 0:
                # User cancelled login, exit app
                sys.exit(0)
            # Only break loop if user is logged in
            if get_current_user_id() != None:
                break

    def handle_logout(self):
        """Handle user logout: update logout time, clear session, show login."""
        if get_current_user_id() != None:
            record_logout( get_current_user_id())
        self.window.hide()
        self.show_login()
        self.window.show()

    def show_table(self, table_name: str):
        # Prevent actions if not logged in
        if not get_current_user_id() != None:
            return
        controller = TableViewController(table_name)
        controller.exec()

    def show_invoice_dialog(self):
        if not get_current_user_id() != None:
            return
        invoice_controller = InvoiceController(self.window)
        invoice_controller.generate_invoice()

    def show_settings_dialog(self):
        if not get_current_user_id() != None:
            return
        self.settings_controller.show_settings()

    def run(self):
        """Run the main application loop, ensuring logout time is updated on exit."""
        self.show_login()
        self.window.show()
        try:
            self.app.exec()
        finally:
            # On app exit, update logout time if user is logged in
            if get_current_user_id() != None:
                record_logout( get_current_user_id())
                self.handle_logout()
                sys.exit(0)  # Ensure app exits cleanly after logout