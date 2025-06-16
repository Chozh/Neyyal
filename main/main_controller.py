import sys
from PyQt6.QtWidgets import QApplication
from login.login_controller import LoginController
from TableView.tableview_controller import TableViewController
from .main_view import MainWindow
from invoice.invoice_controller import InvoiceController
from settings.settings_controller import SettingsController

class MainController:
    def __init__(self, app: QApplication):
        self.app = app
        self.app.setApplicationName("Angadi Billing System")
        self.window = MainWindow()
        self.setup_menu_connections()
        self.settings_controller = SettingsController(self.app)

    def setup_menu_connections(self) -> None:
        # Menu actions
        self.window.exit_action.triggered.connect(self.app.quit)  # type: ignore
        self.window.users_action.triggered.connect(lambda: self.show_table("users"))  # type: ignore
        self.window.login_history_action.triggered.connect(lambda: self.show_table("login_history"))  # type: ignore
        self.window.generate_invoice_action.triggered.connect(self.show_invoice_dialog)  # type: ignore

        # Toolbar actions
        self.window.settings_action.triggered.connect(self.show_settings_dialog)  # type: ignore

        # Show login dialog on startup
        #self.show_login()

    def show_login(self) -> None:
        login = LoginController(self.window)
        if login.exec() == 0:
            # User cancelled login, exit app
            sys.exit(0)
        # On successful login, continue to show main window

    def show_table(self, table_name: str):
        controller = TableViewController(table_name)
        controller.exec()

    def show_invoice_dialog(self):
        invoice_controller = InvoiceController(self.window)
        invoice_controller.generate_invoice()

    def show_settings_dialog(self):
        self.settings_controller.show_settings()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())
