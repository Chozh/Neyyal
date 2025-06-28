# style_global_light.py - Light mode global styles for Neyyal

BUTTON_STYLE_LIGHT = """
QPushButton {
    font-size: 18px;
    font-weight: bold;
    background: #fff;
    color: #22b8be;
    border: 2px solid #22b8be;
    border-radius: 6px;
    padding: 6px 18px;
}
QPushButton:hover {
    background: #22b8be;
    color: #fff;
}
QPushButton:pressed {
    background: #176d72;
    color: #fff;
}
"""

LABEL_STYLE_LIGHT = """
QLabel {
    font-size: 16px;
    color: #222;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-weight: 500;
    letter-spacing: 0.5px;
    padding: 2px 4px;
    background: transparent;
    border: none;
}
QLabel[role="title"] {
    font-size: 22px;
    font-weight: bold;
    color: #22b8be;
    letter-spacing: 1px;
    padding: 6px 0 8px 0;
}
QLabel[role="subtitle"] {
    font-size: 18px;
    color: #888;
    font-style: italic;
    padding: 2px 0 6px 0;
}
"""

EDIT_STYLE_LIGHT = """
QLineEdit, QTextEdit {
    font-size: 16px;
    background: #f8f9fa;
    border: 1px solid #22b8be;
    border-radius: 4px;
    padding: 4px 8px;
    color: #222;
    selection-background-color: #22b8be;
    selection-color: #fff;
}
QLineEdit:focus, QTextEdit:focus {
    border-color: #22b8be;
    background: #fff;
}
QLineEdit[echoMode="Password"] {
    font-family: "Courier New", monospace;
}
"""

TABLE_STYLE_LIGHT = """
QTableWidget, QTableView {
    background: #fff;
    color: #222;
    gridline-color: #bbb;
    selection-background-color: #22b8be;
    selection-color: #fff;
    border-radius: 4px;
}
QHeaderView::section {
    background: #f8f9fa;
    color: #22b8be;
    font-weight: bold;
    border: 1px solid #22b8be;
    padding: 4px;
}
"""

MENU_STYLE_LIGHT = """
QMenuBar {
    background: #f8f9fa;
    color: #222;
    font-size: 16px;
    font-family: 'Segoe UI', Arial, sans-serif;
    border: none;
}
QMenuBar::item {
    background: transparent;
    color: #222;
    padding: 6px 18px;
    margin: 0 2px;
}
QMenuBar::item:selected {
    background: #22b8be;
    color: #fff;
    border-radius: 4px;
}
QMenuBar::item:pressed {
    background: #176d72;
    color: #fff;
}

QMenu {
    background: #fff;
    color: #222;
    border: 1px solid #22b8be;
    font-size: 15px;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QMenu::item {
    background: transparent;
    color: #222;
    padding: 6px 24px 6px 24px;
    border-radius: 4px;
}
QMenu::item:selected {
    background: #22b8be;
    color: #fff;
}
QMenu::separator {
    height: 1px;
    background: #bbb;
    margin: 4px 0;
}
"""

TOOLBAR_STYLE_LIGHT = """
QToolBar {
    background: #f8f9fa;
    border-bottom: 1px solid #22b8be;
    spacing: 6px;
    padding: 4px 8px;
}
QToolButton {
    background: transparent;
    color: #222;
    font-size: 16px;
    font-family: 'Segoe UI', Arial, sans-serif;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
}
QToolButton:hover {
    background: #22b8be;
    color: #fff;
}
QToolButton:pressed {
    background: #176d72;
    color: #fff;
}
"""

WINDOW_STYLE_LIGHT = """
QMainWindow, QWidget {
    background: #fff;
    color: #222;
    font-family: 'Segoe UI', Arial, sans-serif;
}
"""

DATE_EDIT_STYLE_LIGHT = """
QDateEdit {
    background: #f8f9fa;
    color: #222;
    border: 1px solid #22b8be;
    border-radius: 4px;
    padding: 4px 8px;
}
QDateEdit::drop-down {
    background: #22b8be;
    color: #181c1f;
    border: none;
    border-radius: 4px;
}
QDateEdit::drop-down:hover {
    background: #176d72;
}
"""

COMBO_BOX_STYLE_LIGHT = """
QComboBox {
    background: #f8f9fa;
    color: #222;
    border: 1px solid #22b8be;
    border-radius: 4px;
    padding: 4px 8px;
}
QComboBox::drop-down {
    background: #22b8be;
    color: #181c1f;
    border: none;
    border-radius: 4px;
}
QComboBox::drop-down:hover {
    background: #176d72;
}
"""

CHECKBOX_STYLE_LIGHT = """
QCheckBox {
    background: #f8f9fa;
    color: #222;
    border: 1px solid #22b8be;
    border-radius: 4px;
    padding: 4px 8px;
}
QCheckBox::indicator {
    background: #22b8be;
    border: none;
    border-radius: 4px;
}
QCheckBox::indicator:checked {
    background: #176d72;
}
"""

RADIO_BUTTON_STYLE_LIGHT = """
QRadioButton {
    background: #f8f9fa;
    color: #222;
    border: 1px solid #22b8be;
    border-radius: 4px;
    padding: 4px 8px;
}
QRadioButton::indicator {
    background: #22b8be;
    border: none;
    border-radius: 4px;
}
QRadioButton::indicator:checked {
    background: #176d72;
}
"""

PROGRESS_BAR_STYLE_LIGHT = """
QProgressBar {
    background: #f8f9fa;
    border: 1px solid #22b8be;
    border-radius: 4px;
    padding: 4px;
}
QProgressBar::chunk {
    background: #22b8be;
    border-radius:4px;
}
"""

# Combine all styles into a single light theme style
STYLE_LIGHT = (
    BUTTON_STYLE_LIGHT +
    LABEL_STYLE_LIGHT +
    EDIT_STYLE_LIGHT +
    TABLE_STYLE_LIGHT +
    MENU_STYLE_LIGHT +
    TOOLBAR_STYLE_LIGHT +
    WINDOW_STYLE_LIGHT +
    DATE_EDIT_STYLE_LIGHT +
    COMBO_BOX_STYLE_LIGHT +
    CHECKBOX_STYLE_LIGHT +
    RADIO_BUTTON_STYLE_LIGHT +
    PROGRESS_BAR_STYLE_LIGHT
)