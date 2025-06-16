"""
main.py - Entry point for Angadi Billing System
"""

from main.main_controller import MainController
from settings.settings_controller import SettingsController
from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # Set global stylesheet
    SettingsController.apply_global_styles(app)  # Default to dark mode
    app.setApplicationName("Angadi Billing System")
    # Initialize main controller
    controller = MainController(app)
    controller.run()
