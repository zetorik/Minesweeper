from PySide6.QtWidgets import QVBoxLayout,QLayout
from random import randint
from .constants import COLORS

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