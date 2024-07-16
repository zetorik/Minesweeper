from PySide6.QtWidgets import QPushButton,QSizePolicy,QLineEdit,QLabel,QVBoxLayout
from PySide6.QtGui import QIcon,QIntValidator
from PySide6.QtCore import Qt
from threading import Thread
from time import sleep
from .ui_utils import int_to_3

class TileButton(QPushButton):
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(0,0)
        self.set_default_style()
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu  )
    
    def set_default_style(self):
        self.setStyleSheet("background-color: #3c3c3c ; border-width: 0px; font-size: 20pt; font-family: VT323; border-radius:1; ")
        self.setEnabled(True)
        self.setIcon(QIcon())
    


class SettingLine(QLineEdit):
    def __init__(self) -> None:
        super().__init__()
        
        int_validator = QIntValidator()
        self.setValidator(int_validator)
        

class RBLabel(QLabel):
    def __init__(self,text):
        super().__init__(text=text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(40)
        self.setMaximumWidth(80)
        self.setStyleSheet('background-color: black; border-radius: 5px; color: red; font-size: 30pt; font-family: VT323;')

class RBTimer(RBLabel):
    def __init__(self, text):
        super().__init__(text)
        self.time:int = 0
        self.timer_thread = Thread(target=self.timer,daemon=True)
        self.running = False
    
    def timer(self):
        self.time = 0
        while self.running == True:
            sleep(1)
            if not self.running:
                break
            self.time += 1
            
            self.setText(int_to_3(self.time))
            

    def start_timer(self):
        self.running = True
        self.timer_thread.start()
        
    
    def stop_timer(self):
        self.running = False
        


class UtilButton(QPushButton):
    def __init__(self,icon,icon_size):
        super().__init__(icon=icon)
        self.setFixedSize(30,30)
        self.setIconSize(icon_size)

class TileEdit(QLineEdit):
    def __init__(self,old_value:int=0):
        super().__init__()

        self.old_value = old_value
        self.setMinimumSize(0,0)
        self.default_style = "background-color: #3c3c3c ; border-width: 0px; font-size: 20pt; font-family: VT323; border-radius: 0; "
        self.setStyleSheet(self.default_style)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        int_validator = QIntValidator()
        self.setValidator(int_validator)

        self.icon_label = QLabel(self)
        self.icon_label.setStyleSheet('background-color: rgba(0, 0, 0, 0);')  # Transparent background

        self.l = QVBoxLayout(self)
        self.l.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.l.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the icon_label
        self.l.addWidget(self.icon_label)