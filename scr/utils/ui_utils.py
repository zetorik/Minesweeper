from PySide6.QtWidgets import QVBoxLayout,QLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette,QColor
from random import randint

from .constants import COLORS

dark_palette = QPalette()

dark_palette.setColor(QPalette.Window, QColor(37, 37, 38))
dark_palette.setColor(QPalette.WindowText, Qt.white)
dark_palette.setColor(QPalette.Base, QColor(30, 30, 30))
dark_palette.setColor(QPalette.AlternateBase, QColor(37, 37, 38))
dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
dark_palette.setColor(QPalette.ToolTipText, Qt.white)
dark_palette.setColor(QPalette.Text, Qt.white)
dark_palette.setColor(QPalette.Button, QColor(45, 45, 48))
dark_palette.setColor(QPalette.ButtonText, Qt.white)
dark_palette.setColor(QPalette.BrightText, Qt.red)
dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
dark_palette.setColor(QPalette.HighlightedText, Qt.black)

def set_enabled_layout(layout: QVBoxLayout, enabled: bool):
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if isinstance(item,QLayout):
            set_enabled_layout(item,enabled)
        widget = item.widget()
        if widget is not None:
            widget.setEnabled(enabled)

def int_to_3(n:int) -> str:
    """
    Convets int to string with min 3 chars like: 1 -> 001, 12 -> 012, 1234 -> 1234
    """
    new_n = str(n)
    if len(new_n) < 3:
        while len(new_n) < 3:
            new_n = '0'+new_n

    return new_n

def get_auto_mines(w:int,h:int,p:int=15) -> int:
    return round(w * h/100 * p)

def generate_random_color() -> str:
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    return f'rgb({r}, {g}, {b})'

def get_color(value:int) -> str:
    return COLORS.get(str(value),generate_random_color())