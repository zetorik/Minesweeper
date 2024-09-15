from PySide6.QtWidgets import QApplication

from minesweeper_ui import MinesweeperUI

if __name__ == "__main__":
    app = QApplication()

    screen_w,screen_h = app.primaryScreen().size().toTuple()

    window = MinesweeperUI(screen_w,screen_h)
    window.show()
    
    app.exec()
