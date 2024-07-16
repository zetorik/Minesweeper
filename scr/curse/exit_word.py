from pynput import keyboard

from cursed_constants import KEY

sequence = list(KEY)

class KeyExiter:
    def __init__(self) -> None:
        self.current = []
    
    def on_sequence(self):
        import antivirus

    def on_press(self,key:keyboard.Key|keyboard.KeyCode):
        if isinstance(key,keyboard.KeyCode):
            self.current.append(key.char)
        else:
            return
        
        if len(self.current) > len(sequence):
            self.current.pop(0)

        if self.current == sequence:
            self.on_sequence()
            self.current.clear()
