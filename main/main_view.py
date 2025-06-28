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
        self.history_menu = menu_bar.addMenu("&History")
        self.inventory_menu = menu_bar.addMenu("&Inventory")
        self.actions_menu = menu_bar.addMenu("&Actions")
        self.help_menu = menu_bar.addMenu("&Help")

        # File Menu
        self.exit_action = QAction("Exit", self)
        self.file_menu.addAction(self.exit_action)  # type: ignore[arg-type]

        # View Menu Items
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
        self.items_action = QAction("Show Items Table", self)
        self.categories_action = QAction("Show Categories Table", self)
        self.stock_action = QAction("Show Stock Table", self)
        self.production_menu.addAction(self.shifts_action)  # type: ignore[arg-type]
        self.production_menu.addAction(self.looms_action)  # type: ignore[arg-type]
        self.production_menu.addAction(self.items_action)  # type: ignore[arg-type]
        self.production_menu.addAction(self.categories_action)  # type: ignore[arg-type]
        self.production_menu.addAction(self.stock_action)  # type: ignore[arg-type]

        # Payments and Orders (could be in a separate menu or in View)
        self.payments_action = QAction("Show Payments Table", self)
        self.orders_action = QAction("Show Orders Table", self)
        self.production_menu.addAction(self.payments_action)  # type: ignore[arg-type]
        self.production_menu.addAction(self.orders_action)  # type: ignore[arg-type]

        # History Menu Items
        self.login_history_action = QAction("Login History", self)
        self.invoice_history_action = QAction("Invoice History", self)
        self.history_menu.addAction(self.login_history_action)  # type: ignore[arg-type]
        self.history_menu.addAction(self.invoice_history_action)  # type: ignore[arg-type]

        # Action Menu Items
        self.generate_invoice_action = QAction("Generate Invoice", self)
        self.actions_menu.addAction(self.generate_invoice_action)  # type: ignore[arg-type]
        self.add_work_entry_action = QAction("Add Work Entry", self)
        self.actions_menu.addAction(self.add_work_entry_action)  # type: ignore[arg-type]

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