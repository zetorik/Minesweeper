import sys
from pathlib import Path
import json

from .tile import Tile

file_dir = Path(__file__).parent.parent

if getattr(sys, 'frozen', False):
    exe_dir = Path(sys.executable).parent
else:
    exe_dir = file_dir

config = str(exe_dir / 'config.json')
with open(config,'r') as file:
    dictionaries = json.load(file)

SETS:dict = dictionaries[0]
COLORS:dict = dictionaries[1]
SECRETS:dict = dictionaries[2]
TILE_MAP = list[list[Tile]]
TILE_SIZE = 20