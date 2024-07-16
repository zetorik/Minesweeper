from pathlib import Path

file_dir = Path(__file__).parent
res_path = file_dir/'cursed_res'
secret_files_path = file_dir/'secret_files'

final_cock = str(res_path/'final_cock.mp4')
grandpa_and_egg = str(res_path/'grandpa_and_egg.mp3')
virus = str(res_path/'virus.mp3')

bob = str(res_path/'bob.png')
patrick = str(res_path/'patrick.png')
john_pork = str(res_path/'john_pork.png')
penguin = str(res_path/'penguin.png')
tapok = str(res_path/'tapok.png')
vlad = str(res_path/'vlad.jpg')
platon = str(res_path/'platon.jpg')

secret_bob = secret_files_path/'BOB'
secret_trojan = secret_files_path/'trojan.trojanhorsing'

antivirus_exe = file_dir/'antivirus.exe'
antivirus_py = file_dir/'antivirus.py'

if antivirus_exe.exists():
    antivirus = str(antivirus_exe)
elif antivirus_py.exists():
    antivirus = str(antivirus_py)