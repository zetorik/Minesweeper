from PySide6.QtWidgets import (QApplication,QMainWindow,QStackedWidget,QHBoxLayout,QVBoxLayout,QRadioButton,QWidget,QLabel,QCheckBox,
                               QLineEdit,QTextEdit,QLayout,QPushButton,QGridLayout)
from PySide6.QtGui import QFontDatabase,QIcon,QPixmap
from PySide6.QtCore import QSize,Qt

from game import Minesweeper,MinesweeperMapGenerator
from utils.widgets import SettingLine,TileEdit
from utils.resources import techies,techies_mine,start_icon,retur,cool_font
from utils.map_converter import bob_map_to_map, map_to_bob_map, binary_to_map
from utils.tile import Tile
from utils.ui_utils import set_enabled_layout,get_auto_mines,get_color,dark_palette
from utils.constants import TILE_SIZE

class MapCreatorUI(QMainWindow):
    def __init__(self, screen_w:int=1920, screen_h:int=1080) -> None:
        super().__init__()
        self.qtechies = QIcon(techies)
        self.qtechies_mine = QIcon(techies_mine)
        self.qstart_icon = QIcon(start_icon)
        self.qretur = QIcon(retur)
        
        QFontDatabase.addApplicationFont(cool_font)
        self.setWindowTitle('Map creator')
        self.setWindowIcon(self.qtechies)

        self.menu_size = QSize(250,450)

        self.stacked_widget = QStackedWidget()

        self.width_value = 0
        self.height_value = 0
        self.mines_value = 0

        self.screen_w = screen_w
        self.screen_h = screen_h

        self.auto_n = False

        self.menu_container = QWidget()
        self.stacked_widget.addWidget(self.menu_container)
        self.map_editor_container = QWidget()
        self.stacked_widget.addWidget(self.map_editor_container)

        self.setCentralWidget(self.stacked_widget)

        self.menu_UI()

    def create_offset_layout(self,item:QWidget | QLayout,space:int=20) -> QHBoxLayout:
        new_Hlayout = QHBoxLayout()
        new_Hlayout.addSpacing(space)
        if isinstance(item, QWidget):
            new_Hlayout.addWidget(item)
        elif isinstance(item, QLayout):
            new_Hlayout.addLayout(item)
        return new_Hlayout
    
    def menu_UI(self) -> None:
        self.map_type:int|None = None
        
        menu_layout = QVBoxLayout()

        generate_new_button = QRadioButton('Generate new map')
        generate_new_button.toggled.connect(lambda checked: self.set_start_generate() if checked else None)
        
        generate_new_layout0 = QVBoxLayout()

        self.custom_width_line = SettingLine()
        self.custom_width_line.textEdited.connect(lambda text: self.update_setting(text,self.set_width) )

        self.custom_height_line = SettingLine()
        self.custom_height_line.textEdited.connect(lambda text: self.update_setting(text,self.set_height)  )

        self.custom_mines_line = SettingLine()
        self.custom_mines_line.textEdited.connect(lambda text: self.update_setting(text,self.set_mines) )

        self.auto_mines_checkbox = QCheckBox()
        self.auto_mines_checkbox.toggled.connect(self.set_auto_mines)

        generate_new_layout0.addWidget(QLabel('Width'))
        generate_new_layout0.addWidget(self.custom_width_line)

        generate_new_layout0.addWidget(QLabel('Height'))
        generate_new_layout0.addWidget(self.custom_height_line)

        generate_new_layout0.addWidget(QLabel('Mines'))
        generate_new_layout0.addWidget(self.custom_mines_line)

        generate_new_layout0.addWidget(QLabel('Auto mines'))
        generate_new_layout0.addWidget(self.auto_mines_checkbox)

        self.generate_new_layout = self.create_offset_layout(generate_new_layout0)

        load_from_binary_button = QRadioButton('Load map from binary string')
        load_from_binary_button.toggled.connect(lambda checked: self.set_start_binary() if checked else None)
        self.binary_box = QTextEdit()
        binary_box_layout = self.create_offset_layout(self.binary_box)
        
        load_from_bobmap_button = QRadioButton('Load map from bobmap')
        load_from_bobmap_button.toggled.connect(lambda checked:self.set_start_bob() if checked else None)
        self.bob_map_box = QLineEdit()
        bob_map_box_layout = self.create_offset_layout(self.bob_map_box)

        start_button = QPushButton(icon=self.qstart_icon)
        start_button.setFixedSize(50,50)
        start_button.setIconSize(QSize(25,25))
        start_button.clicked.connect(self.map_creator_ui)

        menu_layout.addWidget(generate_new_button)
        menu_layout.addLayout(self.generate_new_layout)

        menu_layout.addWidget(load_from_binary_button)
        menu_layout.addLayout(binary_box_layout)
        menu_layout.addWidget(load_from_bobmap_button)
        menu_layout.addLayout(bob_map_box_layout)
        menu_layout.addWidget(start_button,alignment=Qt.AlignmentFlag.AlignRight)

        self.set_width(9)
        self.set_height(9)
        self.set_mines(10)

        self.set_none()

        self.menu_container.setLayout(menu_layout)
        self.set_menu_tab()
    
    def set_menu_tab(self):
        self.resize(self.menu_size)
        self.setMinimumSize(self.menu_size)
        self.stacked_widget.setCurrentWidget(self.menu_container)

    def set_none(self):
        set_enabled_layout(self.generate_new_layout,False)
        self.binary_box.setEnabled(False)
        self.bob_map_box.setEnabled(False)

    def set_start_generate(self):
        self.map_type = 1
        set_enabled_layout(self.generate_new_layout,True)
        self.binary_box.setEnabled(False)
        self.bob_map_box.setEnabled(False)

        self.set_auto_mines(self.auto_mines_checkbox.isChecked())

    def set_start_binary(self):
        self.map_type = 2
        set_enabled_layout(self.generate_new_layout,False)
        self.binary_box.setEnabled(True)
        self.bob_map_box.setEnabled(False)

    def set_start_bob(self):
        self.map_type = 3
        set_enabled_layout(self.generate_new_layout,False)
        self.binary_box.setEnabled(False)
        self.bob_map_box.setEnabled(True)

    def set_auto_game_size(self,tile_size:int=TILE_SIZE) -> None:
        t = tile_size + 2
        w,h = self.game.width * t + 10*2 ,  self.game.height*t + 30 + 10*2 + 15 + 20
        
        while w > self.screen_w or h > self.screen_h:
            w = round(w*0.75)
            h = round(h*0.75)

        self.setMinimumSize(1,1)
        self.resize(w,h)

    def map_creator_ui(self):
        if not self.map_type:
            return
        self.map = None
        self.game = Minesweeper()
        
        if self.map_type == 1:
            self.game.generator = MinesweeperMapGenerator(self.width_value,self.height_value,self.mines_value)
            self.game.generate_tile_map()
        elif self.map_type == 2:
            self.game.set_map_data( binary_to_map(self.binary_box.toPlainText()) )
        elif self.map_type == 3:
            self.game.set_map_data( bob_map_to_map( self.bob_map_box.text() ) )
        else:
            return
        
        self.set_auto_game_size()
        self.game.print()
        
        map_editor_layout = QVBoxLayout()
        self.tile_layout = QGridLayout()
        self.tile_layout.setSpacing(1)
        
        for tile in self.game.get_tiles():
            
            tile_edit = TileEdit()
            tile_edit.textEdited.connect(self.tile_edited)
            tile_edit.customContextMenuRequested.connect(self.toggle_mine)
            self.tile_layout.addWidget(tile_edit,*tile.get_pos()) 
            self.update_tile_edit(tile_edit)
        
        buttons_layout = QHBoxLayout()

        retur_button = QPushButton(icon=self.qretur)
        retur_button.setMaximumSize(30,30)
        retur_button.clicked.connect(self.set_menu_tab )
        
        auto_n_checkbox = QCheckBox(text='auto numbers')
        auto_n_checkbox.toggled.connect(self.toggle_auto_n)

        buttons_layout.addWidget(auto_n_checkbox,alignment=Qt.AlignmentFlag.AlignLeft)
        buttons_layout.addWidget(retur_button,alignment=Qt.AlignmentFlag.AlignRight)

        bob_map_LABEL = QLabel(text='bobmap:')

        self.bob_map_text = QLineEdit()
        self.bob_map_text.setReadOnly(True)
        self.update_bob_map_text()
        
        map_editor_layout.addLayout(self.tile_layout)
        map_editor_layout.addLayout(buttons_layout)
        map_editor_layout.addWidget(bob_map_LABEL)
        map_editor_layout.addWidget(self.bob_map_text)
        
        self.stacked_widget.removeWidget(self.map_editor_container)
        self.map_editor_container = QWidget()
        self.map_editor_container.setLayout(map_editor_layout)
        
        self.stacked_widget.addWidget(self.map_editor_container)
        self.stacked_widget.setCurrentWidget(self.map_editor_container)

    def toggle_auto_n(self,state:bool):
        if state == True:
            self.game.put_right_numbers()
            self.update_bob_map_text()
        
        self.auto_n = state
        self.update_all_tile_edits()
    
    def update_bob_map_text(self):
        bobmap = map_to_bob_map(self.game.map_data)
        self.bob_map_text.setText(bobmap)

    def toggle_mine(self):
        tile_edit:TileEdit = self.sender()
        tile = self.tile_edit_to_tile(tile_edit)
        if tile.value == -1:
            tile.value = tile_edit.old_value
        else:
            tile_edit.old_value = tile.value
            tile.value = -1

        if self.auto_n == True:
            for n_tile in self.game.get_neighbor_tiles(tile):
                if n_tile.value != -1:
                    self.game.put_right_number(n_tile)
                    self.update_tile_edit(self.tile_to_edit_tile(n_tile))

        self.update_tile_edit(tile_edit)
        self.update_bob_map_text()
        
    def update_tile_edit(self,tile_edit:TileEdit):
        tile = self.tile_edit_to_tile(tile_edit)
        if tile.value == -1:
            tile_edit.setText('')
            tile_edit.setReadOnly(True)
            tile_edit.setStyleSheet(tile_edit.default_style.replace('#3c3c3c','#4f4f4f'))
            tile_edit.icon_label.setPixmap( self.qtechies_mine.pixmap(QSize(20,20) ) )
        else:
            if tile_edit.text() != str(tile.value):
                tile_edit.setText(str(tile.value))
            tile_edit.setStyleSheet(tile_edit.default_style + f'color: {get_color(tile.value)}; ')
            
            tile_edit.setReadOnly(self.auto_n)
            
            
            tile_edit.icon_label.setPixmap(QPixmap())
    
    def update_all_tile_edits(self):
        for tile in self.game.get_tiles():
            edit_tile = self.tile_to_edit_tile(tile)
            self.update_tile_edit(edit_tile)

    def update_tiles(self,tiles:list[TileEdit]):
        for edit_tile in tiles:
            self.update_tile_edit(edit_tile)

    def tile_edit_to_tile(self,tile_edit:TileEdit) -> Tile:
        row,column,_,_ = self.tile_layout.getItemPosition(self.tile_layout.indexOf(tile_edit))
        
        return self.game.get_tile(row,column)
    
    def tile_to_edit_tile(self,tile:Tile) -> TileEdit:
        return self.tile_layout.itemAtPosition(*tile.get_pos()).widget()

    def tile_edited(self,text:str):
        try:
            value = int(text)
        except:
            return
        
        tile_edit:TileEdit = self.sender()
        tile = self.tile_edit_to_tile(tile_edit)
        tile.value = value

        self.update_tile_edit(tile_edit)
        self.update_bob_map_text()
        

    def update_setting(self,text:str,setter):
        if text.isdigit():
            setter(int(text))

    def set_width(self,value:int):
        self.width_value =value
        self.custom_width_line.setText(str(value))
        if self.auto_mines_checkbox.isChecked():
            self.set_mines(self.get_auto_mines())
    
    def set_height(self,value:int):
        self.height_value = value
        self.custom_height_line.setText(str(value))
        if self.auto_mines_checkbox.isChecked():
            self.set_mines(self.get_auto_mines())
        
    
    def set_mines(self,value:int):
        
        if value == None:
            return
        
        self.custom_mines_line.setText(str(value))
        self.mines_value = value
        
    def get_auto_mines(self) -> int:
        return get_auto_mines(self.width_value,self.height_value)

    def set_auto_mines(self,state:bool) -> None:
        if state == True:
            self.custom_mines_line.setEnabled(False)
            mines = self.get_auto_mines()
            if not mines:
                return
            self.set_mines(mines)
        else:
            self.custom_mines_line.setEnabled(True)


if __name__ == '__main__':
    app = QApplication()
    app.setPalette(dark_palette)
    screen_w,screen_h = app.primaryScreen().size().toTuple()
    window = MapCreatorUI(screen_w,screen_h)
    window.show()
    app.exec()
