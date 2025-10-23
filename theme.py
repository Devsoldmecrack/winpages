from PySide6.QtGui import QColor, QLinearGradient, QPalette
from PySide6.QtCore import Qt

# Dark blue / gray palette
NAVY_1 = QColor(18, 24, 38)      # top gradient
NAVY_2 = QColor(14, 20, 32)      # middle
NAVY_3 = QColor(10, 14, 24)      # bottom
DARK_BG = QColor(12, 16, 24)
DARK_CARD = QColor(24, 30, 44)
DARK_SHEET = QColor(20, 24, 34)
TEXT_PRIMARY = QColor(235, 239, 245)
TEXT_SECONDARY = QColor(150, 170, 200)


def gradient_background(widget):
    g = QLinearGradient(0, 0, 0, widget.height())
    g.setColorAt(0.0, NAVY_1)
    g.setColorAt(0.5, NAVY_2)
    g.setColorAt(1.0, NAVY_3)
    return g


def apply_dark_palette(app):
    p = QPalette()
    p.setColor(QPalette.Window, DARK_BG)
    p.setColor(QPalette.WindowText, TEXT_PRIMARY)
    p.setColor(QPalette.Base, QColor(10, 14, 22))
    p.setColor(QPalette.AlternateBase, DARK_CARD)
    p.setColor(QPalette.ToolTipBase, DARK_CARD)
    p.setColor(QPalette.ToolTipText, TEXT_PRIMARY)
    p.setColor(QPalette.Text, TEXT_PRIMARY)
    p.setColor(QPalette.Button, DARK_CARD)
    p.setColor(QPalette.ButtonText, TEXT_PRIMARY)
    p.setColor(QPalette.BrightText, QColor(255, 80, 80))
    p.setColor(QPalette.Highlight, QColor(70, 120, 200))
    p.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(p)


PRIMARY_BUTTON_QSS = """
QPushButton {
    background-color: rgb(70, 120, 200);
    color: white;
    border-radius: 12px;
    padding: 10px 16px;
    font-weight: 600;
}
QPushButton:hover { background-color: rgb(90, 140, 220); }
QPushButton:pressed { background-color: rgb(60, 110, 190); }
"""

CARD_QSS = """
QFrame {
    background-color: rgb(24,30,44);
    border-radius: 16px;
}
"""

SHEET_QSS = """
QFrame {
    background-color: rgba(18, 24, 38, 190);
    border-radius: 24px;
}
"""

MENU_QSS = """
QMenu {
    background-color: rgb(24,30,44);
    color: rgb(235,239,245);
    border: 1px solid rgb(40,50,70);
    border-radius: 8px;
}
QMenu::item {
    padding: 6px 12px;
    border-radius: 6px;
}
QMenu::item:selected {
    background-color: rgb(36,44,62);
}
QMenu::separator {
    height: 1px;
    background: rgb(40,50,70);
    margin: 4px 6px;
}
"""

SEARCH_QSS = """
QLineEdit {
  background: rgb(20,26,38);
  color: rgb(235,239,245);
  border: 1px solid rgb(40,50,70);
  border-radius: 10px;
  padding: 6px 10px;
}
QLineEdit:focus {
  border: 1px solid rgb(70,120,200);
}
"""

EDITOR_TOOLBAR_QSS = """
QToolBar {
  background: transparent;
  border: none;
}
QToolBar QToolButton {
  background: transparent;
  color: rgb(235,239,245);
  padding: 6px;
  border-radius: 6px;
}
QToolBar QToolButton:hover {
  background: rgba(36,44,62, 1);
}
QToolBar QToolButton:pressed, QToolBar QToolButton:checked {
  background: rgba(28,36,52, 1);
}
"""
