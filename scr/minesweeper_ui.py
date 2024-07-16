from PySide6.QtWidgets import QMainWindow,QPushButton,QHBoxLayout,QVBoxLayout,QListWidget,QWidget,QSizePolicy,QLineEdit,QLabel,QCheckBox,QGridLayout,QSpacerItem,QStackedWidget,QMessageBox
from PySide6.QtGui import QIcon,QFontDatabase
from PySide6.QtCore import Qt,QSize,QTimer
import subprocess
import sys
from threading import Thread

from game import Minesweeper,MinesweeperMapGenerator
from utils.tile import Tile
from utils.resources import cool,flag,hint,icon,skull,smile,mine,techies,techies_mine,start_icon,retur,cool_font,cursed_icon
from utils.constants import SETS,TILE_SIZE,SECRETS,file_dir
from utils.ui_utils import int_to_3,get_auto_mines,get_color
from utils.widgets import TileButton,SettingLine,RBLabel,RBTimer,UtilButton
from utils.map_converter import bob_map_to_map

class MinesweeperUI(QMainWindow):
    """
    Class for creating and changing user interface in minesweeper game
    """
    def __init__(self, screen_w:int=1920, screen_h:int=1080):
        super().__init__()
        self.qcool = QIcon(cool)
        self.qflag = QIcon(flag)
        self.qhint = QIcon(hint)
        self.qicon = QIcon(icon)
        self.qskull = QIcon(skull)
        self.qsmile = QIcon(smile)
        self.qmine = QIcon(mine)
        self.qtechies = QIcon(techies)
        self.qtechies_mine = QIcon(techies_mine)
        self.qstart_icon = QIcon(start_icon)
        self.qretur = QIcon(retur)
        self.qcursed = QIcon(cursed_icon)

        QFontDatabase.addApplicationFont(cool_font)
        
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.no_guess_value = False

        self.width_value = 0
        self.height_value = 0
        self.mines_value = 0

        self.reset_button = None
        self.timer = None
        self.game = None

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.menu_container = QWidget()
        self.stacked_widget.addWidget(self.menu_container)
        self.game_container = QWidget()
        self.stacked_widget.addWidget(self.game_container)
        self.start_container = QWidget()
        self.stacked_widget.addWidget(self.start_container)

        self.menu_size = QSize(300,350)

        self.setWindowTitle('Minesweeper')
        self.setWindowIcon(self.qicon)
        
        self.start_UI()

    def start_UI(self):
        start_ui_layout = QVBoxLayout()
        play_layout = QHBoxLayout()
        
        start_text = QLabel(text='Welcome to Bob Minesweeper!1!11!')
        start_text.setStyleSheet('font-family: VT323;  font-size: 50pt; color: red')
        start_text.setMinimumHeight(300)

        self.play_button = QPushButton(text='Play')
        self.play_button.setStyleSheet('font-family: VT323; color: green; font-size: 20pt;')
        self.play_button.clicked.connect(self.menu_UI)

        self.dplay_button = QPushButton(text='Dont play')
        self.dplay_button.setStyleSheet('font-family: VT323; color: red; font-size: 20pt;')
        self.dplay_button.clicked.connect(self.dplay_clicked)

        play_layout.addWidget(self.play_button)
        play_layout.addWidget(self.dplay_button)

        start_ui_layout.addWidget(start_text)
        start_ui_layout.addLayout(play_layout)

        self.start_container.setLayout(start_ui_layout)

        self.switch_tab(self.start_container)

    def dplay_clicked(self):
        oldtext = self.play_button.text()
        oldstyle = self.play_button.styleSheet()
        
        self.play_button.setText(self.dplay_button.text())
        self.play_button.setStyleSheet(self.dplay_button.styleSheet())
        
        self.dplay_button.setText(oldtext)
        self.dplay_button.setStyleSheet(oldstyle)

        QTimer.singleShot(200,self.menu_UI)
    
    def menu_UI(self):
        self.show_custom_mines = False
        self.cursed = False
        
        self.setMinimumSize(self.menu_size)
        self.resize(self.menu_size)

        start_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        
        start_list = QListWidget()
        start_list.addItems(['Beginner', 'Intermediate', 'Expert', 'Custom'])
        start_list.currentTextChanged.connect(self.dificulty_changed)
        
        self.custom_width = QLineEdit()
        self.custom_width.textEdited.connect(self.set_width)

        self.custom_height = QLineEdit()
        self.custom_height.textEdited.connect(self.set_height)

        self.custom_mines = SettingLine()
        self.custom_mines.textEdited.connect(self.set_mines)
        
        start_button = QPushButton()
        start_button.setIcon(self.qstart_icon)
        start_button.setFixedSize(80,80)
        start_button.setIconSize(QSize(30,30))
        start_button.clicked.connect(lambda:self.start_game())

        guess_checkbox = QCheckBox(text='No guess mode')
        guess_checkbox.toggled.connect(self.guess_checkbox_toggled)

        show_custom_mines_checkbox = QCheckBox(text='Show mines on custom maps')
        show_custom_mines_checkbox.toggled.connect(self.show_custom_mines_checkbox_toggled)

        cursed_checkbox = QCheckBox(text='وضع الديك الملعون')
        cursed_checkbox.toggled.connect(self.cursed_checkbox_toggled)

        self.auto_mines_checkbox = QCheckBox(text='Auto mines')
        self.auto_mines_checkbox.setEnabled(False)
        self.auto_mines_checkbox.clicked.connect(self.set_auto_mines)

        left_layout.setSpacing(5)
        left_layout.addWidget(start_list,2)

        left_layout.addWidget(QLabel('Width'),0.5)
        left_layout.addWidget(self.custom_width,1)

        left_layout.addWidget(QLabel('Height'),0.5)
        left_layout.addWidget(self.custom_height,1)

        left_layout.addWidget(QLabel('Mines'),0.5)
        left_layout.addWidget(self.custom_mines,1)

        left_layout.addWidget(self.auto_mines_checkbox,1)
        left_layout.addWidget(guess_checkbox,1)
        left_layout.addWidget(show_custom_mines_checkbox,1)
        left_layout.addWidget(cursed_checkbox,1)
        
        start_layout.addLayout(left_layout)
        start_layout.addWidget(start_button)
        start_layout.setAlignment(start_button,Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self.menu_container.setLayout(start_layout)
        self.switch_tab(self.menu_container)

        self.enable_custom_settings(False)


    def get_auto_mines(self) -> int:
        return get_auto_mines(self.width_value,self.height_value)

    def set_auto_mines(self,state:bool) -> None:
        
        if state == True:
            self.custom_mines.setEnabled(False)
            self.set_mines(self.get_auto_mines())
        else:
            self.custom_mines.setEnabled(True)

    def guess_checkbox_toggled(self,state:bool):
        self.no_guess_value = state

    def show_custom_mines_checkbox_toggled(self,state:bool):
        self.show_custom_mines = state

    def cursed_checkbox_toggled(self,state:bool):
        self.cursed = state

    def switch_tab(self,tab:QWidget) -> None:
        self.stacked_widget.setCurrentWidget(tab)

        if tab == self.menu_container:
            self.setMinimumSize(self.menu_size)
            self.resize(self.menu_size)


    def enable_custom_settings(self,state:bool) -> None:
        self.custom_width.setEnabled(state)
        self.custom_height.setEnabled(state)
        self.custom_mines.setEnabled(state)
        self.auto_mines_checkbox.setEnabled(state)
        if state == False:
            self.auto_mines_checkbox.setChecked(False)

    def dificulty_changed(self,dif:str) -> None: # change settings when user chooses another dificulty
        self.dificulty = dif
        
        if dif == 'Custom':
            self.enable_custom_settings(True)
            
        else:
            self.enable_custom_settings(False)
            M_set = SETS.get(dif)
            self.set_width(M_set[0])
            self.set_height(M_set[1])
            self.set_mines(M_set[2])

    def set_setting_text(self,setting:str,value:int, setting_text:QLineEdit) -> None: # function for better organization
        if isinstance(value,str):
            if value.isdigit():
                value = int(value)
            else:
                return
        
        setattr(self,setting,value)
        if setting_text.text() != str(value):
            setting_text.setText(str(value))

        
    def set_width(self,value:int) -> None:
        self.set_setting_text('width_value',value,self.custom_width)

        if self.auto_mines_checkbox.isChecked() == True:
            self.set_mines(self.get_auto_mines())

    def set_height(self,value:int) -> None:
        self.set_setting_text('height_value',value,self.custom_height)

        if self.auto_mines_checkbox.isChecked() == True:
            self.set_mines(self.get_auto_mines())
    def set_mines(self,value:int) -> None:
        self.set_setting_text('mines_value',value,self.custom_mines)
        self.reset_button

    def set_auto_game_size(self,tile_size:int=TILE_SIZE) -> None:
        t = tile_size + 2
        w,h = self.game.width * t + 10*2 ,  self.game.height*t + 40 + 30 + 10*2 + 15 # 10 - offset, 40 - h of top menu, 30 - h of bot menu, 15 - offset
        
        while w > self.screen_w or h > self.screen_h:
            w = round(w*0.75)
            h = round(h*0.75)

        self.setMinimumSize(1,1)
        self.resize(w,h)

    def start_game(self,resize=True) -> None:
        self.board_ready = False
        self.custom_map = False
        
        if self.mines_value > self.width_value * self.height_value:
            self.mines_value = self.width_value * self.height_value

        self.game = Minesweeper()
        
        if not self.custom_height.text().isdigit():
            secret = self.custom_height.text()
        else:
            secret = SECRETS.get(self.custom_width.text(),None)

        if secret:
            self.game.set_map_data(bob_map_to_map(secret))
            self.board_ready = True
            self.custom_map = True
        else:
            self.game.generator = MinesweeperMapGenerator(self.width_value,self.height_value,self.mines_value,no_guess=self.no_guess_value)
            self.generate_map()
        self.game.print()
        
        if resize == True:
            self.set_auto_game_size()
        
        self.game.start_game()
        
        game_layout = QVBoxLayout()
        
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(20)

        self.mines_left_label = RBLabel(text=int_to_3(self.game.mines_left))

        self.reset_button = QPushButton(icon=self.qsmile)
        self.reset_button.setFixedSize(40,40)
        self.reset_button.setIconSize(QSize(25,25))
        self.reset_button.clicked.connect(lambda:( self.disable_ingame(),self.start_game(resize=False)))

        self.timer = RBTimer(text='000')

        menu_layout.addWidget(self.mines_left_label,8)
        menu_layout.addWidget(self.reset_button,5)
        menu_layout.addWidget(self.timer,8)

        self.mine_layout = QGridLayout()
        self.mine_layout.setSpacing(1)

        for tile in self.game.get_tiles():
            
            tile_button = TileButton() 
            tile_button.clicked.connect(self.tile_button_click)
            tile_button.customContextMenuRequested.connect(self.tile_button_right_click)
            self.mine_layout.addWidget(tile_button,*tile.get_pos())     
        
        utility_layout = QHBoxLayout()

        self.hint_button = UtilButton(icon=self.qhint,icon_size=QSize(25,25))
        self.hint_button.clicked.connect(self.hint )

        return_button = UtilButton(icon=self.qretur, icon_size=QSize(15,15))
        return_button.clicked.connect(lambda:( self.disable_ingame(), self.switch_tab(self.menu_container) ) ) 
        
        utility_layout.addSpacerItem(QSpacerItem(100,30,QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed))
        utility_layout.addWidget(self.hint_button)
        utility_layout.addWidget(return_button)
        
        game_layout.addLayout(menu_layout,1)
        game_layout.addLayout(self.mine_layout,8)
        game_layout.addLayout(utility_layout,1)
        
        self.stacked_widget.removeWidget(self.game_container)

        self.game_container = QWidget()
        self.game_container.setLayout(game_layout)

        self.stacked_widget.addWidget(self.game_container)
        self.switch_tab(self.game_container)
        
    
    def remove_hints(self):
        if self.game.map_data:
            for tile in self.game.remove_hints():
                self.update_button(self.tile_to_button(tile))
        

    def generate_map(self):
        self.remove_hints()
        self.game.generate_tile_map()

    def generate_needed_map(self) -> bool:
        self.remove_hints() 
        return self.game.generate_needed_map()

    def tile_button_click(self):
        if not self.game.game_running:
            return
        
        
        tile_button:TileButton = self.sender()
        tile = self.button_to_tile(tile_button)
        
        if not self.board_ready:
            self.game.generator.start_pos = tile.get_pos()

            if self.game.height * self.game.width == self.game.max_mines:
                self.techies()
                return
            
            if self.generate_needed_map() == False:
                return
            self.board_ready = True
            tile = self.button_to_tile(tile_button)
            
        
        if self.timer.running == False:
            self.timer.start_timer()
        
        result,tiles_to_reveal = self.game.recursive_reveal(tile)
        
        for n_tile in tiles_to_reveal:
            button = self.tile_to_button(n_tile)
            self.update_button(button)
        
        if result == 'win':
            self.win()
        elif result == 'lose':
            self.lose()
    

    def update_button(self,button:TileButton):
        
        tile = self.button_to_tile(button)
        
        button.set_default_style()
        current_style = button.styleSheet()

        if tile.revealed:
            
            button.setEnabled(False)
            
            if tile.value == -1:
                button.setStyleSheet(current_style.replace('#3c3c3c','#c72828'))
            else:
                if tile.value == 0:
                    
                    button.setStyleSheet(current_style.replace('#3c3c3c','#2c2c2f'))

                else:
                    button.setText(str(tile.value))
                    button.setStyleSheet(current_style.replace('#3c3c3c','#2c2c2f') + f'color: {get_color(tile.value)}; ')
        elif tile.flagged:
            button.setIcon(self.qflag)
            button.setIconSize(QSize(20,20))
        elif tile.hinted:
            button.setStyleSheet(current_style.replace('#3c3c3c','#3bb440'))
            if tile.value == -1:
                button.setIcon(self.qflag)
                button.setIconSize(QSize(20,20))


    def tile_button_right_click(self):
        if not self.board_ready or not self.game.game_running:
            return
        
        tile_button:TileButton = self.sender()
        
        tile = self.button_to_tile(tile_button)
        if tile.flagged:
            self.unflag(tile)
        else:
            self.flag(tile)
        self.update_button(tile_button)
    
    def flag(self,tile:Tile):
        tile_button = self.tile_to_button(tile)
        self.game.flag_tile(tile)
        
        
        self.mines_left_label.setText(int_to_3(self.game.mines_left))
        self.update_button(tile_button)

    def unflag(self,tile:Tile):
        tile_button = self.tile_to_button(tile)
        self.game.unflag_tile(tile)
        
        self.mines_left_label.setText(int_to_3(self.game.mines_left))
        self.update_button(tile_button)

    def hint(self):
        if not self.game.game_running:
            return

        hint_tile:Tile = self.game.hint()
        if not hint_tile:
            return
        hint_button = self.tile_to_button(hint_tile)
        self.update_button(hint_button)

    def unhint(self,tile:Tile):
        hint_button = self.tile_to_button(tile)
        self.update_button(hint_button)

    def button_to_tile(self,button:TileButton) -> Tile:
        row,column,_,_ = self.mine_layout.getItemPosition(self.mine_layout.indexOf(button))
        return self.game.get_tile(row,column)
    
    def tile_to_button(self,tile:Tile) -> TileButton:
        return self.mine_layout.itemAtPosition(*tile.get_pos()).widget()


    def disable_ingame(self):
        
        self.game.stop_game()
        self.hint_button.setEnabled(False)
        self.timer.stop_timer()

        for n_tile in self.game.get_tiles():
            if n_tile.hinted == True:
                self.unhint(n_tile)

    def unflag_all(self):
        for n_tile in self.game.get_tiles():
            if n_tile.flagged == True:
                self.unflag(n_tile)

    def set_mines_icons(self,icon:QIcon,size:QSize=QSize(15,15)):
        for n_tile in self.game.get_tiles_with_value(-1):
            n_tile_button = self.tile_to_button(n_tile)
            self.unflag_all()

            if n_tile.value == -1:
                n_tile_button.setIcon(icon)
                n_tile_button.setIconSize(size)

    def lose(self) ->None:
        if self.cursed == True:
            
            self.reset_button.setIcon(self.qcursed)
            msg_box = QMessageBox(text='You need to find an antivirus in 1 of the folders on desktop. You have 10 minutes. Good luck..')
            msg_box.setWindowTitle('YOU LOST :)')
            msg_box.setWindowIcon(self.qcursed)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            curse = file_dir / 'curse'
            starting_point = curse / 'starting_point.exe'
            if starting_point.exists():
                subprocess.Popen([str(starting_point)])

            else:
                starting_point = curse / 'starting_point.py'
                subprocess.Popen([sys.executable, str(starting_point)])
                print('bob')
            
        else:
            self.reset_button.setIcon(self.qskull)
        
        if self.custom_map == False or self.show_custom_mines == True:
            self.set_mines_icons(self.qmine,QSize(15,15))
        
        self.disable_ingame()
            
    def win(self):
        self.reset_button.setIcon(self.qcool)
        
        for n_tile in self.game.get_tiles_with_value(-1):
            if n_tile.flagged == False:
                self.flag(n_tile)

        self.disable_ingame()

    def techies(self):
        self.reset_button.setIcon(self.qtechies)
        self.reset_button.setIconSize(QSize(50,50))

        self.set_mines_icons(self.qtechies_mine,QSize(15,15))

        self.disable_ingame()