# style_global_dark.py - Dark mode global styles for Neyyal

# --- QPushButton dark style ---
BUTTON_STYLE_DARK = """
QPushButton {
    font-size: 18px;
    font-weight: bold;
    background: #222c31;
    color: #22b8be;
    border: 2px solid #22b8be;
    border-radius: 6px;
    padding: 6px 18px;
}
QPushButton:hover {
    background: #22b8be;
    color: #181c1f;
}
QPushButton:pressed {
    background: #176d72;
    color: #fff;
}
"""

# --- QLabel dark style ---
LABEL_STYLE_DARK = """
QLabel {
    font-size: 16px;
    color: #e0e0e0;
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
    color: #b0b0b0;
    font-style: italic;
    padding: 2px 0 6px 0;
}
"""

# --- QLineEdit, QTextEdit dark style ---
EDIT_STYLE_DARK = """
QLineEdit, QTextEdit {
    font-size: 16px;
    background: #181c1f;
    border: 1px solid #22b8be;
    border-radius: 4px;
    padding: 4px 8px;
    color: #e0e0e0;
    selection-background-color: #22b8be;
    selection-color: #181c1f;
}
QLineEdit:focus, QTextEdit:focus {
    border-color: #22b8be;
    background: #23282c;
}
QLineEdit[echoMode="Password"] {
    font-family: "Courier New", monospace;
}
"""

# --- QTableWidget, QTableView dark style ---
TABLE_STYLE_DARK = """
QTableWidget, QTableView {
    background: #181c1f;
    color: #e0e0e0;
    gridline-color: #333;
    selection-background-color: #22b8be;
    selection-color: #181c1f;
    border-radius: 4px;
}
QHeaderView::section {
    background: #23282c;
    color: #22b8be;
    font-weight: bold;
    border: 1px solid #22b8be;
    padding: 4px;
}
"""

# --- QMenuBar, QMenu dark style ---
MENU_STYLE_DARK = """
QMenuBar {
    background: #23282c;
    color: #e0e0e0;
    font-size: 16px;
    font-family: 'Segoe UI', Arial, sans-serif;
    border: none;
}
QMenuBar::item {
    background: transparent;
    color: #e0e0e0;
    padding: 6px 18px;
    margin: 0 2px;
}
QMenuBar::item:selected {
    background: #22b8be;
    color: #181c1f;
    border-radius: 4px;
}
QMenuBar::item:pressed {
    background: #176d72;
    color: #fff;
}
QMenu {
    background: #23282c;
    color: #e0e0e0;
    border: 1px solid #22b8be;
    font-size: 15px;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QMenu::item {
    background: transparent;
    color: #e0e0e0;
    padding: 6px 24px 6px 24px;
    border-radius: 4px;
}
QMenu::item:selected {
    background: #22b8be;
    color: #181c1f;
}
QMenu::separator {
    height: 1px;
    background: #333;
    margin: 4px 0;
}
"""

# --- QToolBar, QToolButton dark style ---
TOOLBAR_STYLE_DARK = """
QToolBar {
    background: #26323a;
    border-bottom: 2px solid #22b8be;
    spacing: 6px;
    padding: 4px 8px;
}
QToolButton {
    background: transparent;
    color: #e0e0e0;
    font-size: 16px;
    font-family: 'Segoe UI', Arial, sans-serif;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
}
QToolButton:hover {
    background: #22b8be;
    color: #181c1f;
}
QToolButton:pressed {
    background: #176d72;
    color: #fff;
}
"""

# --- QMainWindow, QWidget dark style ---
WINDOW_STYLE_DARK = """
QMainWindow, QWidget {
    background: #181c1f;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
}
"""

# --- QDateEdit dark style ---
DATE_EDIT_STYLE_DARK = """
QDateEdit {
    background: #26323a;
    color: #e0e0e0;
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

# --- QComboBox dark style ---
COMBO_BOX_STYLE_DARK = """
QComboBox {
    background: #26323a;
    color: #e0e0e0;
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

# --- QCheckBox dark style ---
CHECKBOX_STYLE_DARK = """
QCheckBox {
    background: #26323a;
    color: #e0e0e0;
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

# --- QRadioButton dark style ---
RADIO_BUTTON_STYLE_DARK = """
QRadioButton {
    background: #26323a;
    color: #e0e0e0;
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

# --- QProgressBar dark style ---
PROGRESS_BAR_STYLE_DARK = """
QProgressBar {
    background: #26323a;
    border: 1px solid #22b8be;
    border-radius: 4px;
    padding: 4px;
}
QProgressBar::chunk {
    background: #22b8be;
    border-radius: 4px;
}
"""

STYLE_DARK = (
    BUTTON_STYLE_DARK +
    LABEL_STYLE_DARK +
    EDIT_STYLE_DARK +
    TABLE_STYLE_DARK +
    MENU_STYLE_DARK +
    TOOLBAR_STYLE_DARK +
    WINDOW_STYLE_DARK +
    DATE_EDIT_STYLE_DARK +
    COMBO_BOX_STYLE_DARK +
    CHECKBOX_STYLE_DARK +
    RADIO_BUTTON_STYLE_DARK +
    PROGRESS_BAR_STYLE_DARK
)