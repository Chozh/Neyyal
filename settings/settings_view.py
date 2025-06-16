from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QWidget

class SettingsDialog(QDialog):
    def __init__(self, current_mode: str, parent: 'QWidget | None' = None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])  # type: ignore
        # Set the current theme mode
        if current_mode not in ["dark", "light"]:
            current_mode = "dark"
        self.theme_combo.setCurrentText(current_mode)
        layout.addWidget(self.theme_combo)
        self.save_btn = QPushButton("Save")
        layout.addWidget(self.save_btn)