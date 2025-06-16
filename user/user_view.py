# user_view.py
from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt6.QtCore import Qt
from typing import Optional

class UserRegistrationDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] =None):
        super().__init__(parent)
        self.setWindowTitle("Admin Registration")
        self.setFixedSize(900, 400)
        self.setStyleSheet("background-color: #22b8be;")

        # Title
        title = QLabel("RESTAURANT BILLING SYSTEM", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: #333;")

        subtitle = QLabel("ADMIN REGISTRATION", self)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")

        # Left fields
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.phone_label = QLabel("Phone No.:")
        self.phone_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Right fields
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.confirmpass_label = QLabel("Confirm Pass:")
        self.confirmpass_input = QLineEdit()
        self.confirmpass_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Required labels
        req_style = "color: #333; font-size: 12px;"
        self.name_req = QLabel("This field is required")
        self.name_req.setStyleSheet(req_style)
        self.phone_req = QLabel("This field is required")
        self.phone_req.setStyleSheet(req_style)
        self.password_req = QLabel("This field is required")
        self.password_req.setStyleSheet(req_style)
        self.username_req = QLabel("This field is required")
        self.username_req.setStyleSheet(req_style)
        self.address_req = QLabel("This field is required")
        self.address_req.setStyleSheet(req_style)
        self.confirmpass_req = QLabel("This field is required")
        self.confirmpass_req.setStyleSheet(req_style)

        # Layouts for left and right columns
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.name_label)
        left_layout.addWidget(self.name_input)
        left_layout.addWidget(self.name_req)
        left_layout.addSpacing(10)
        left_layout.addWidget(self.phone_label)
        left_layout.addWidget(self.phone_input)
        left_layout.addWidget(self.phone_req)
        left_layout.addSpacing(10)
        left_layout.addWidget(self.password_label)
        left_layout.addWidget(self.password_input)
        left_layout.addWidget(self.password_req)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.username_label)
        right_layout.addWidget(self.username_input)
        right_layout.addWidget(self.username_req)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.address_label)
        right_layout.addWidget(self.address_input)
        right_layout.addWidget(self.address_req)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.confirmpass_label)
        right_layout.addWidget(self.confirmpass_input)
        right_layout.addWidget(self.confirmpass_req)

        form_layout = QHBoxLayout()
        form_layout.addLayout(left_layout)
        form_layout.addSpacing(40)
        form_layout.addLayout(right_layout)

        # Register button
        self.register_btn = QPushButton("Register")

        # Login link
        login_layout = QHBoxLayout()
        already_label = QLabel("Already User?")
        self.login_link = QLabel('<a href="#">click here to Login</a>')
        self.login_link.setStyleSheet("color: red; font-weight: bold;")
        self.login_link.setTextFormat(Qt.TextFormat.RichText)
        self.login_link.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.login_link.setOpenExternalLinks(False)
        login_layout.addWidget(already_label)
        login_layout.addSpacing(10)
        login_layout.addWidget(self.login_link)
        login_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(10)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.register_btn)
        main_layout.addSpacing(20)
        main_layout.addLayout(login_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)


    def get_registration_data(self):
        return (
            self.name_input.text(),
            self.username_input.text(),
            self.phone_input.text(),
            self.address_input.text(),
            self.password_input.text(),
            self.confirmpass_input.text()
        )