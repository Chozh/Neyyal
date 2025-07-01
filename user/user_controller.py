# user_controller.py
from PyQt6.QtWidgets import QWidget
from typing import Optional
from .user_model import UserModel, UserRecord
from .user_view import UserRegistrationDialog

class UserController:
    def __init__(self, parent: Optional[QWidget] = None):
        self.model = UserModel()
        self.view = UserRegistrationDialog(parent)
        self.view.register_btn.clicked.connect(self.handle_register)  # type: ignore
        self.view.login_link.linkActivated.connect(self.handle_login_link)  # type: ignore

    def exec(self):
        return self.view.exec()

    def handle_register(self):
        if self.view.verify_input():
            username, password, _ = self.view.get_registration_data()
            user_type = "Admin" if self.view.admin_type.isChecked() else "User"
            # You may want to set added_by and employee_id appropriately
            user = UserRecord(
                username=username,
                password=password,
                user_type=user_type,
                added_by=None,
                employee_id=None
            )
            if self.model.register_user(user):
                self.view.show_message("Success", "User registered successfully!")
                self.view.accept()
            else:
                self.view.show_message("Error", "Failed to register user. Please try again.")

    def handle_login_link(self):
        # Logic to show login dialog
        self.view.accept()

    def get_user_by_id(self, user_id: int):
        return self.model.get_user_by_id(user_id)

    def get_user_by_username(self, username: str):
        return self.model.get_user_by_username(username)
