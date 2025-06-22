# login_controller.py
from PyQt6.QtWidgets import QMessageBox, QWidget
from typing import Optional
from .login_model import UserModel
from .login_view import LoginDialog

class LoginController:
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the LoginController with an optional parent widget."""
        self.parent = parent
        self.model = UserModel()
        self.view = LoginDialog(parent)
        self.view.login_btn.clicked.connect(lambda: self.handle_login())  # type: ignore

    def exec(self):
        return self.view.exec()

    def handle_login(self) -> None:
        """Handle the login process for employee or admin."""
        # Get user credentials from the view
        username, password, _ = self.view.get_credentials()  # Assuming get_credentials is a method in LoginDialog
        if not username or not password:
            QMessageBox.warning(self.view, "Input Error", "Username and password cannot be empty.")
            return
        # Validate user credentials
        if self.model.validate_user(username, password):
            self.view.accept()
            if self.parent is not None:
                self.parent.show()  # Show main window on successful login
        else:
            QMessageBox.warning(self.view, "Login Failed", "Invalid username or password.")

