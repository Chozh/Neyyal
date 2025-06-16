# settings_controller.py - Handles application settings and theme management

from .settings_model import SettingsModel
from .settings_view import SettingsDialog
from utils.style_global import (
    BUTTON_STYLE_DARK, BUTTON_STYLE_LIGHT,
    LABEL_STYLE_DARK, LABEL_STYLE_LIGHT,
    EDIT_STYLE_DARK, EDIT_STYLE_LIGHT,
    TABLE_STYLE_DARK, TABLE_STYLE_LIGHT,
    MENU_STYLE_DARK, MENU_STYLE_LIGHT
)
from PyQt6.QtWidgets import QApplication  # or from PySide2.QtWidgets import QApplication

class SettingsController:
    def __init__(self, app: QApplication):
        self.app = app

    def show_settings(self):
        dlg = SettingsDialog(SettingsModel.get_theme_mode())
        if dlg.exec():
            mode = dlg.theme_combo.currentText()
            SettingsModel.set_theme_mode(mode)
            # Re-apply global styles
            SettingsController.apply_global_styles(self.app)

    @staticmethod
    def apply_global_styles(app: QApplication):
        """
        Apply global styles based on the selected theme mode.
        :param app: QApplication instance
        :param theme_mode: 'dark' or 'light'
        """
        if SettingsModel.get_theme_mode() == 'dark':
            app.setStyleSheet(
                BUTTON_STYLE_DARK +
                LABEL_STYLE_DARK +
                EDIT_STYLE_DARK +
                TABLE_STYLE_DARK +
                MENU_STYLE_DARK
            )
        else:
            app.setStyleSheet(
                BUTTON_STYLE_LIGHT +
                LABEL_STYLE_LIGHT +
                EDIT_STYLE_LIGHT +
                TABLE_STYLE_LIGHT +
                MENU_STYLE_LIGHT
            )