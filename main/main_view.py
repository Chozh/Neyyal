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
        self.view_menu = menu_bar.addMenu("&View")
        self.history_menu = menu_bar.addMenu("&History")
        self.inventory_menu = menu_bar.addMenu("&Inventory")
        self.actions_menu = menu_bar.addMenu("&Actions")

        self.exit_action = QAction("Exit", self)
        if self.file_menu is not None:
            self.file_menu.addAction(self.exit_action)  # type: ignore[arg-type]
        
        # View Menu Items
        self.users_action = QAction("Show Users Table", self)
        self.shifts_action = QAction("Show Shifts Table", self)
        self.looms_action = QAction("Show Looms Table", self)
        if self.view_menu is not None:
            self.view_menu.addAction(self.users_action)  # type: ignore[arg-type]
            self.view_menu.addSeparator()
            self.view_menu.addAction(self.shifts_action)  # type: ignore[arg-type]
            self.view_menu.addSeparator()
            self.view_menu.addAction(self.looms_action)  # type: ignore[arg-type]

        # History Menu Items
        self.login_history_action = QAction("Login History", self)
        self.invoice_history_action = QAction("Invoice History", self)
        if self.history_menu is not None:
            self.history_menu.addAction(self.login_history_action)  # type: ignore[arg-type]
            self.history_menu.addSeparator()
            self.history_menu.addAction(self.invoice_history_action)  # type: ignore[arg-type]

        # Action Menu Items
        self.generate_invoice_action = QAction("Generate Invoice", self)
        self.actions_menu.addAction(self.generate_invoice_action)  # type: ignore[arg-type]
        self.add_work_entry_action = QAction("Add Work Entry", self)
        self.actions_menu.addAction(self.add_work_entry_action)  # type: ignore[arg-type]

        # Right toolbar for settings and logout icons
        toolbar = QToolBar()
        toolbar.setStyleSheet("QToolBar { background: transparent; border: none; }")
        
        # Create a spacer widget to push the buttons to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Create the settings action
        self.settings_action = QAction(QIcon("Icons/settings.png"), "Settings", self)
        self.settings_action.setObjectName("settings_action")
        self.settings_action.setToolTip("Application Settings")

        # Create the logout action
        self.logout_action = QAction(QIcon("Icons/logout.png"), "Logout", self)
        self.logout_action.setObjectName("logout_action")
        self.logout_action.setToolTip("Logout from the application")

        # Add the spacer, settings, and logout actions to the toolbar
        toolbar.addWidget(spacer)
        toolbar.addAction(self.settings_action)  # type: ignore[arg-type]
        toolbar.addAction(self.logout_action)    # type: ignore[arg-type]
        # Set the icon size for the toolbar actions
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