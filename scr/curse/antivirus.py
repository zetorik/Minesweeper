import subprocess
from win32com.shell import shell, shellcon # type: ignore
import shutil
from pathlib import Path

DESKTOP = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)

a = 'æ'
desktop_path = Path(DESKTOP)

for root,dirs,files in desktop_path.walk():
    print(dirs)
    for dir_name in dirs:
        if a in dir_name:
            dir_path = desktop_path/dir_name
            shutil.rmtree(str(dir_path))

    for file_name in files:
        if a in file_name:
            file_path = desktop_path/file_name
            file_path.unlink()

VIRUSES = [
    'starting_point.exe'
]
running_processes = subprocess.check_output(['tasklist'], universal_newlines=True)

found_exe = False
for virus in VIRUSES:
    if virus.lower() in running_processes.lower():
        subprocess.call(f'taskkill /F /IM "{virus}"')
        found_exe = True
if not found_exe:
    subprocess.call(f'taskkill /F /IM "python.exe"')

