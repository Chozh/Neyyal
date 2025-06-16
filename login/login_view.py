# view.py
from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QLineEdit, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from typing import Optional

class LoginDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("Icon/shop.png"))
        self.setFixedSize(400, 300)

        # Welcome label
        self.welcome_label = QLabel("Welcome to Angadi Billing System!", self)
        self.welcome_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # User type radio buttons
        self.employee_radio = QRadioButton("Employee", self)
        self.admin_radio = QRadioButton("Admin", self)
        self.employee_radio.setChecked(True)  # Default select to employee
        self.user_type_group = QButtonGroup(self)
        self.user_type_group.addButton(self.employee_radio)
        self.user_type_group.addButton(self.admin_radio)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.employee_radio)
        radio_layout.addWidget(self.admin_radio)

        # Username and password labels and textboxes
        self.username_label = QLabel("Username:", self)
        self.username_input = QLineEdit(self)
        self.password_label = QLabel("Password:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)

        # Login button
        self.login_btn = QPushButton("Login", self)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.welcome_label)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(radio_layout)  # Move radio buttons here, after password input
        main_layout.addWidget(self.login_btn)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def get_credentials(self) -> tuple[str, str, str]:
        """
        Retrieve the username, password, and user type from the input fields.
        Returns:
            tuple: (username: str, password: str, user_type: str)
        """
        username = self.username_input.text()
        password = self.password_input.text()
        user_type = "employee" if self.employee_radio.isChecked() else "admin"
        return username, password, user_type