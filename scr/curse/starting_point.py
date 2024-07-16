from PySide6.QtWidgets import QApplication
from pynput import mouse,keyboard

from cursed_files import create_files
from cursed_loops import start_loops
from cursed_screen import CursedWindow
from cockroach_window import CockroachWindow
from artifact_window import ArtifactWindow
from key_sound import ReleaseSound
from exit_word import KeyExiter

def on_key_press(*args):
        key_exiter.on_press(*args)
    
def on_key_release(*args):
    release_sound.on_release(*args)

def on_mouse_click(*args):
    artifact_window.on_click(*args)

def on_mouse_move(*args):
    artifact_window.on_move(*args)

if __name__ == '__main__':
    create_files()
    start_loops()
    release_sound = ReleaseSound()
    key_exiter = KeyExiter()
    
    app = QApplication()
    
    cursed_window = CursedWindow()
    cursed_window.start()
    cursed_window.show()

    cockroach_window = CockroachWindow()
    cockroach_window.start()
    cockroach_window.show()

    artifact_window  = ArtifactWindow()
    artifact_window.show()

    mouse_listener = mouse.Listener(on_click=on_mouse_click,on_move=on_mouse_move)
    keyboard_listener = keyboard.Listener(on_press=on_key_press,on_release=on_key_release)
    mouse_listener.start()
    keyboard_listener.start()

    app.exec()
