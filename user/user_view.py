# user_view.py
from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QSizePolicy
)
from PyQt6.QtCore import Qt
from user_model import UserModel
from configuration import APPLICATION_NAME
from typing import Optional

class UserRegistrationDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] =None):
        super().__init__(parent)
        self.model = UserModel()  # Initialize the user model
        self.setWindowTitle("User Registration")
        self.setFixedSize(900, 400)

        # Title
        title = QLabel(APPLICATION_NAME, self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("USER REGISTRATION", self)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmpass_label = QLabel("Confirm Pass:")
        self.confirmpass_input = QLineEdit()
        self.confirmpass_input.setEchoMode(QLineEdit.EchoMode.Password)
        #  add radio button for user type Admin or User
        self.user_type_label = QLabel("User Type:")
        self.user_type_input = QWidget()
        self.user_type_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # Radio buttons for user type
        self.admin_type = QRadioButton("Admin")
        self.admin_type.setChecked(False)
        self.admin_type.toggled.connect(lambda: self.user_type.setChecked(not self.admin_type.isChecked()))  # type: ignore

        self.user_type = QRadioButton("User")
        self.user_type.setChecked(True)
        self.user_type.toggled.connect(lambda: self.admin_type.setChecked(not self.user_type.isChecked()))  # type: ignore

        # Layout for user type radio buttons
        self.user_type_input_layout = QHBoxLayout(self.user_type_input)
        self.user_type_input_layout.addWidget(self.user_type_label)
        self.user_type_input_layout.addWidget(self.admin_type)
        self.user_type_input_layout.addWidget(self.user_type)
        self.user_type_input_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.user_type_input_layout.setContentsMargins(0, 0, 0, 0)
        self.user_type_input_layout.setSpacing(20)
        self.user_type_input_layout.addStretch()


        # Required labels
        req_style = "color: #333; font-size: 12px;"
        self.password_req = QLabel("This field is required")
        self.password_req.setStyleSheet(req_style)
        self.username_req = QLabel("This field is required")
        self.username_req.setStyleSheet(req_style)
        self.confirmpass_req = QLabel("This field is required")
        self.confirmpass_req.setStyleSheet(req_style)

        # Layouts for left and right columns
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.password_label)
        left_layout.addWidget(self.password_input)
        left_layout.addWidget(self.password_req)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.username_label)
        right_layout.addWidget(self.username_input)
        right_layout.addWidget(self.username_req)
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
            self.username_input.text(),
            self.password_input.text(),
            self.confirmpass_input.text()
        )

    def show_message(self, msg_type: str, message: str):
        """Show an error message dialog."""
        from PyQt6.QtWidgets import QMessageBox
        if msg_type.lower() == "success":
            QMessageBox.information(self, "Success", message, QMessageBox.StandardButton.Ok)
        elif msg_type.lower() == "warning":
            QMessageBox.warning(self, "Warning", message, QMessageBox.StandardButton.Ok)
        else:
            # Default to warning
            QMessageBox.warning(self, "Error", message, QMessageBox.StandardButton.Ok)

    def verify_input(self) -> bool:
        username, password, confirmpass = self.get_registration_data()
        if not all([username, password, confirmpass]):
            self.show_message("error", "All fields are required.")
            return False
        if password != confirmpass:
            self.show_message("error", "Passwords do not match.")
            return False
        if hasattr(self, 'model') and self.model.user_exists(username):
            self.show_message("error", "Username already exists.")
            return False
        if hasattr(self, 'is_password_strong') and not self.is_password_strong(password):
            self.show_message("error", "Password must be at least 8 characters long and include letters, numbers, and special characters.")
            return False
        return True
        
    def is_password_strong(self, password: str) -> bool:
        """Check if the password meets strength criteria."""
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isalpha() for char in password):
            return False
        if not any(char in "!@#$%^&*()-_=+[]|;:,.<>?/" for char in password):
            return False
        return True