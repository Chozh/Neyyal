"""
main.py - Entry point for Neyyal Production Management System
"""

from main.main_controller import MainController
from settings.settings_controller import SettingsController
from PyQt6.QtWidgets import QApplication
from configuration import COMPANY_NAME

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setOrganizationName(COMPANY_NAME)
    app.setApplicationName("Neyyal Production Management System")
    # Initialize main controller
    controller = MainController(app)
    controller.run()
