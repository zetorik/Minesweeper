from PySide6.QtWidgets import QLabel,QMainWindow
from PySide6.QtGui import QPixmap,QPainter,QColor
from PySide6.QtCore import Qt
from pynput import mouse
from random import randint,choice

from cursed_constants import ARTIFACTS

class ArtifactWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput |Qt.WindowType.WindowStaysOnTopHint) 

        self.start_x,self.start_y = None,None
        self.mouse_down = False
        self.current_artifact = choice(ARTIFACTS)
        
        self.showFullScreen()
        self.setWindowOpacity(0.5)

        self.label = QLabel()

        self.setCentralWidget(self.label)

        canvas = QPixmap(self.size())
        self.label.setPixmap(canvas)

    def draw_artifact(self,x1:int,y1:int):
        if  self.start_x is None or self.start_y is None:
            return
        
        x = min(self.start_x,x1)
        y = min(self.start_y,y1)
        
        width = abs(self.start_x-x1)
        height = abs(self.start_y-y1)
        
        canvas = self.label.pixmap()
        bob_pixmap = QPixmap(self.current_artifact).scaled(width,height)
        painter = QPainter(canvas)
        painter.setBrush(bob_pixmap)
        painter.setPen(Qt.NoPen)
        painter.drawRect(x,y,width,height)

        overlay_color = QColor(randint(0,255),randint(0,255),randint(0,255),128)
        painter.setBrush(overlay_color)
        painter.drawRect(x,y,width,height)
        painter.end()
        self.label.setPixmap(canvas)
        
    def on_click(self,x:int, y:int, button:mouse.Button, pressed:bool):
        if button == mouse.Button.left:
            self.mouse_down = pressed
            if pressed:
                self.start_x,self.start_y = x,y
            else:
                self.current_artifact = choice(ARTIFACTS)

    def on_move(self,x,y):
        if self.mouse_down and self.start_x is not None:
            self.draw_artifact(x,y)




