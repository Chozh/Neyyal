# user_controller.py
from PyQt6.QtWidgets import QMessageBox, QWidget
from typing import Optional
from .user_model import UserModel
from .user_view import UserRegistrationDialog

class UserController:
    def __init__(self, parent: Optional[QWidget] =None):
        self.model = UserModel()
        self.view = UserRegistrationDialog(parent)
        self.view.register_btn.clicked.connect(self.handle_register)  # type: ignore
        self.view.login_link.linkActivated.connect(self.handle_login_link)  # type: ignore

    def exec(self):
        return self.view.exec()

    def handle_register(self):
        name, username, phone, address, password, confirmpass, user_type = self.view.get_registration_data()
        # Basic validation
        if not all([name, username, phone, address, password, confirmpass]):
            QMessageBox.warning(self.view, "Validation Error", "All fields are required.")
            return
        if password != confirmpass:
            QMessageBox.warning(self.view, "Validation Error", "Passwords do not match.")
            return
        if self.model.user_exists(username):
            QMessageBox.warning(self.view, "Validation Error", "Username already exists.")
            return
        if not self.is_password_strong(password):
            QMessageBox.warning(self.view, "Validation Error", "Password must be at least 8 characters long and include letters, numbers, and special characters.")
            return
        if user_type == "ADMIN":
            if self.model.register_admin(name, username, phone, address, password):
                QMessageBox.information(self.view, "Success", " Admin Registration successful!")
                self.view.accept()
            else:
                QMessageBox.critical(self.view, "Error", "Registration failed.")
        elif user_type == "EMP":
            if self.model.register_employee(name, username, phone, address, password):
                QMessageBox.information(self.view, "Success", "Employee Registration successful!")
                self.view.accept()
            else:
                QMessageBox.critical(self.view, "Error", "Registration failed.")

    def handle_login_link(self):
        # Logic to show login dialog
        QMessageBox.information(self.view, "Login", "Show login dialog here.")
        self.view.accept()

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
