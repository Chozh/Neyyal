from PyQt6.QtWidgets import QMainWindow, QMenuBar, QToolBar, QWidget, QSizePolicy, QVBoxLayout
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import QtCore
from configuration import COMPANY_NAME, ICON_PATH

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(COMPANY_NAME)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setGeometry(100, 100, 1080, 768)

        # Central Widget and Layout
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Native menu bar
        menu_bar = self.menuBar()
        if menu_bar is None:
            menu_bar = QMenuBar(self)
            self.setMenuBar(menu_bar)
        self.file_menu = menu_bar.addMenu("&File")
        self.people_menu = menu_bar.addMenu("&People")
        self.production_menu = menu_bar.addMenu("&Production")
        self.inventory_menu = menu_bar.addMenu("&Inventory")
        self.invoice_menu = menu_bar.addMenu("&Invoice")
        self.history_menu = menu_bar.addMenu("&History")
        self.reports_menu = menu_bar.addMenu("&Reports")
        self.help_menu = menu_bar.addMenu("&Help")

        # File Menu
        self.exit_action = QAction("Exit", self)
        self.file_menu.addAction(self.exit_action)  # type: ignore[arg-type]

        # People Menu Items
        self.users_action = QAction("Show Users Table", self)
        self.employees_action = QAction("Show Employees Table", self)
        self.customers_action = QAction("Show Customers Table", self)
        self.suppliers_action = QAction("Show Suppliers Table", self)
        self.people_menu.addAction(self.users_action)  # type: ignore[arg-type]
        self.people_menu.addAction(self.employees_action)  # type: ignore[arg-type]
        self.people_menu.addAction(self.customers_action)  # type: ignore[arg-type]
        self.people_menu.addAction(self.suppliers_action)  # type: ignore[arg-type]

        # Production Menu Items
        self.shifts_action = QAction("Show Shifts Table", self)
        self.looms_action = QAction("Show Looms Table", self)
        self.add_work_entry_action = QAction("Add Work Entry", self)
        self.production_menu.addAction(self.shifts_action)  # type: ignore[arg-type]
        self.production_menu.addAction(self.looms_action)  # type: ignore[arg-type]
        self.production_menu.addAction(self.add_work_entry_action)  # type: ignore[arg-type]


        # Inventory Menu Items
        self.items_action = QAction("Show Items Table", self)
        self.categories_action = QAction("Show Categories Table", self)
        self.stock_action = QAction("Show Stock Table", self)
        self.inventory_menu.addAction(self.items_action)  # type: ignore[arg-type]
        self.inventory_menu.addAction(self.categories_action)  # type: ignore[arg-type]
        self.inventory_menu.addAction(self.stock_action)  # type: ignore[arg-type]

        # Invoice Menu Items
        self.sales_orders_action = QAction("Show Sales Orders Table", self)
        self.purchase_orders_action = QAction("Show Purchase Orders Table", self)
        self.payments_action = QAction("Show Payments Table", self)
        self.generate_invoice_action = QAction("Generate Invoice", self)
        self.inventory_menu.addAction(self.payments_action)  # type: ignore[arg-type]
        self.inventory_menu.addAction(self.sales_orders_action)  # type: ignore[arg-type]
        self.inventory_menu.addAction(self.purchase_orders_action)  # type: ignore[arg-type]
        self.inventory_menu.addAction(self.generate_invoice_action)  # type: ignore[arg-type]

        # History Menu Items
        self.login_history_action = QAction("Login History", self)
        self.invoice_history_action = QAction("Invoice History", self)
        self.history_menu.addAction(self.login_history_action)  # type: ignore[arg-type]
        self.history_menu.addAction(self.invoice_history_action)  # type: ignore[arg-type]

        # Reports Menu Items
        self.sales_report_action = QAction("Sales Report", self)
        self.purchase_report_action = QAction("Purchase Report", self)
        self.production_report_action = QAction("Production Report", self)
        self.reports_menu.addAction(self.sales_report_action)  # type: ignore[arg-type]
        self.reports_menu.addAction(self.purchase_report_action)  # type: ignore[arg-type]
        self.reports_menu.addAction(self.production_report_action)  # type: ignore[arg-type]

        # Right toolbar for settings and logout icons
        toolbar = QToolBar()
        toolbar.setStyleSheet("QToolBar { background: transparent; border: none; }")
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.settings_action = QAction(QIcon("Icons/settings.png"), "Settings", self)
        self.settings_action.setObjectName("settings_action")
        self.settings_action.setToolTip("Application Settings")
        self.logout_action = QAction(QIcon("Icons/logout.png"), "Logout", self)
        self.logout_action.setObjectName("logout_action")
        self.logout_action.setToolTip("Logout from the application")
        toolbar.addWidget(spacer)
        toolbar.addAction(self.settings_action)  # type: ignore[arg-type]
        toolbar.addAction(self.logout_action)    # type: ignore[arg-type]
        toolbar.setIconSize(QtCore.QSize(24, 24))
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, toolbar)

    def set_content(self, widget: QWidget):
        """Helper method to clear and set the central widget content."""
        for i in reversed(range(self.central_layout.count())):
            item = self.central_layout.itemAt(i)
            if item is not None:
                old_widget = item.widget()
                if old_widget is not None:
                    old_widget.deleteLater()
        self.central_layout.addWidget(widget)

    def show_message(self, title: str, message: str):
        """Show a message box with the given title and message."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, title, message)