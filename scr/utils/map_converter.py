from .constants import TILE_MAP
from .tile import Tile

def binary_to_map(binary:str) -> TILE_MAP:
    tile_map = [[]]

    row = 0
    column = 0
    for c in binary:
        if c == '\n':
            tile_map.append([])
            row+=1
            column=0
            continue

        value = 0
        if c =='1':
            value = -1
        
        tile_map[row].append( Tile(value,row,column) )
        column+=1

    return tile_map

def map_to_bob_map(tile_map:TILE_MAP) -> str:
    bobmap:str = ''

    for row in tile_map:
        if tile_map.index(row) == 0:
            bobmap += 'b'
        else:
            bobmap += 'bb'
        
        for tile in row:
            bobmap += 'o'
            bobmap += str(tile.value)
            bobmap += 'o'
    bobmap += 'b'
    
    return bobmap

def bob_map_to_map(bobmap:str) -> TILE_MAP:
    tile_map:TILE_MAP = [[]]

    row = 0
    col = 0
    values = []
    for i,c in enumerate(bobmap):
        if i == len(bobmap)-1 or i == 0:
            continue
        next_c = bobmap[i+1]
        prev_c = bobmap[i-1]

        if c == 'b' and next_c == 'b':
            tile_map.append([])
            row += 1
            col = 0
            continue

        if c.isdigit() or c=='-':
            values.append(c)

        if c == 'o' and prev_c != 'o' and prev_c != 'b' :
            try:
                value = int(''.join(values) )
                tile_map[row].append( Tile(value,row,col ))
                col += 1
            except:
                print(f'invalid bob part {i}')
            
            values = []
    
    return tile_map