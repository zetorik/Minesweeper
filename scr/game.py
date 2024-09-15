from random import randint
from copy import deepcopy

from utils.map2d import Map2D
from utils.tile import Tile
from utils.constants import TILE_MAP

class Minesweeper(Map2D):
    """
    Class for tile and game logic
    """

    def __init__(self,tile_map:TILE_MAP=None ) :
        super().__init__(map_data=tile_map)
        self.game_running = False
        self.mines_left = 0
        self.generator:MinesweeperMapGenerator = None

    def print_revealed_flagged(self):
        for row in self.map_data:
            for tile in row:
                tile:Tile
                if tile.revealed == True:
                    c = str(tile.value)
                elif tile.flagged == True:
                    c = 'f'
                else:
                    c = 'n'
                print(c,end='')
            print()
        print(' ')


    def generate_tile_map(self):
        self.generator.generate_tile_map()
        self.set_map_data(self.generator.minesweeper.map_data)

    def generate_needed_map(self):
        result = self.generator.generate_needed_map()
        if result:
            if self.map_data != self.generator.minesweeper.map_data:
                self.set_map_data(self.generator.minesweeper.map_data)
        
        return result
        
    
    def start_game(self):
        self.game_running = True
        self.max_mines = len(self.get_tiles_with_value(-1))
        self.mines_left = self.max_mines

    def stop_game(self):
        
        self.game_running = False
        self.mines_left = 0

    def put_right_number(self,tile:Tile) -> bool:
        if tile.value != -1:
            new_value = len(self.get_neighbors_with_value(tile,-1))
            if tile.value != new_value:
                tile.value = new_value
                return True
        
        return False
    
    def put_right_numbers(self) -> list[Tile]:
        affected_tiles = []
        for tile in self.get_tiles():
            if self.put_right_number(tile) == True:
                affected_tiles.append(tile)
        
        return affected_tiles

    def hint(self) -> Tile:
        """
        Gives user hint (shows wheres 0 tile if it exists, if no then shows wheres closest mine)
        """
        
        hint_tile = self._get_first_unrevealed_0_tile()
        
        if not hint_tile: 
            hint_tile = self._get_hint_mine()
        
        if not hint_tile:
            hint_tile - self._get_hint_tile()

        if not hint_tile:
            return

        self.hint_tile(hint_tile)
        return hint_tile

    def _get_hint_tile(self):
        tiles = self.get_tiles()
        return self._get_hint_of(tiles)

    
    def get_tiles(self) -> list[Tile]:
        return self.get_all_objects()
    
    def get_tiles_with_value(self,value:int) -> list[Tile]:
        return [tile for tile in self.get_tiles() if tile.value == value]
    
    def get_hinted_tiles(self) -> list[Tile]:
        return [tile for tile in self.get_tiles() if tile.hinted == True]
    
    def get_tile(self,row:int,column:int) -> Tile:
        return self.get_object(row,column)
    
    def get_neighbor_tiles(self,tile:Tile) -> list[Tile]:
        return self.get_neighbor_objects(tile)
    
    def get_neighbors_with_value(self,tile:Tile,value:int) -> list[Tile]:
        return [n_tile for n_tile in self.get_neighbor_tiles(tile) if n_tile.value == value]
    
    def reveal_tile(self,tile:Tile,user:bool=True) -> bool:

        if (tile.revealed == True) or ( tile.flagged == True and user == True ) or (tile.hinted == True and tile.value == -1):
            return False
        

        if tile.hinted == True:
            self.unhint_tile(tile)

        if tile.flagged == True:
            self.unflag_tile(tile)      
        
        tile.revealed = True
        return True
    
    def flag_tile(self,tile:Tile) -> bool:
        if (tile.hinted == True and tile.value != -1) or self.mines_left <= 0:
            return False
        
        if tile.hinted:
            self.unhint_tile(tile)
        self.mines_left -= 1
        tile.flagged = True
        return True
    
    def unflag_tile(self,tile:Tile) -> None:
        self.mines_left +=1
        tile.flagged = False

    def hint_tile(self,tile:Tile) -> None:
        
        tile.hinted = True

    def unhint_tile(self,tile:Tile) -> None:
        
        tile.hinted = False
    
    def recursive_reveal(self,tile:Tile) -> tuple[str,list[Tile]] :
        """
        Reveals tile, if its 0 then starts 'recursive' chain of revealing. Returns tuple with first agr: 'default', if won: 'win', if lost: 'lose', second agr: all tiles that were revealed.
        """

        
        tiles_to_reveal = [tile]
        revealed_tiles = []
        result = 'default'

        while tiles_to_reveal:
            
            current_tile = tiles_to_reveal.pop()
            revealed_tiles.append(current_tile)
            
            user = False
            if current_tile == tile:
                user = True

            if self.reveal_tile(current_tile,user) == True :
                
                if self.check_win():
                    result = 'win'
                    break
                if current_tile.value == -1:
                    result = 'lose'
                    break
                
                if current_tile.value == 0:
                    for n_tile in self.get_neighbor_tiles(current_tile):
                        if n_tile.value != -1:
                            
                            tiles_to_reveal.append(n_tile)

        return (result,revealed_tiles)
                

    
    def check_win(self) -> bool: 
        tilecheck = True
        

        for n_tile in self.get_tiles():
            if n_tile.value != -1:
                if n_tile.revealed == False:
                    tilecheck = False
        
        return tilecheck
    
    def _get_revealed_tiles(self) -> list[Tile]:
        revealed_tiles = []

        for n_tile in self.get_tiles():
            if n_tile.revealed == True:
                revealed_tiles.append(n_tile)
        
        return revealed_tiles
    


    def _smallest_distance_to_revealed_tile(self,tile:Tile) -> int:
        revealed_tiles = self._get_revealed_tiles()

        if not revealed_tiles:
            return 616
        
        distances = [self.get_distance(tile,n_tile) for n_tile in revealed_tiles]
        distances.sort()
    
        return distances[0]
    
    def _get_hint_of(self,tile_list:list[Tile]) -> Tile:
        tile_list = [tile for tile in tile_list if tile.flagged == False and tile.revealed == False]

        if not tile_list:
            return
        
        return min(tile_list,key=self._smallest_distance_to_revealed_tile)
    
    def remove_hints(self) -> list[Tile]:
        removed_tiles = []
        for tile in self.get_tiles():
            if tile.hinted:
                self.unhint_tile(tile)
                removed_tiles.append(tile)
        return removed_tiles
    
    def _get_hint_mine(self) -> Tile:
        mines = self.get_tiles_with_value(-1)
        
        return self._get_hint_of(mines)
        
    def _get_first_unrevealed_0_tile(self) -> Tile | None:    
        for n_tile in self.get_tiles():
            if n_tile.value == 0 and n_tile.revealed == False:
                return n_tile
        return None
    
    def int_list_to_tile_map(self,list:list[list[int]]) -> TILE_MAP:
        return [ [Tile(n,ir,ic ) for ic,n in enumerate(row)   ] for ir,row in enumerate(list)  ]

class MinesweeperMapGenerator:
    """
    Class for generating minesweeper maps
    """

    def __init__(self,width:int,height:int,num_mines:int,start_pos:tuple[int,int]=None,no_guess:bool=False):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.start_pos = start_pos
        self.no_guess = no_guess
        self.minesweeper = None
        
    # -1 - mine,other numbers - tiles
    def generate_tile_map(self) -> None : 
        tile_map:TILE_MAP = [[Tile(0,r,c) for c in range(self.width)] for r in range(self.height)]
        self.minesweeper = Minesweeper(tile_map)
        
        # put mines
        for _ in range(0,self.num_mines): 
            while True:
                
                r_row = randint(0,self.height - 1)
                r_pos = randint(0,self.width - 1)

                tile:Tile = self.minesweeper.get_tile(r_row,r_pos)

                if self.start_pos:
                    if tile.get_pos() == self.start_pos:
                        continue
                    
                    if self.no_guess:
                        start_tile:Tile = self.minesweeper.get_tile(*self.start_pos)
                        if tile in self.minesweeper.get_neighbor_tiles(start_tile):
                            continue
                
                if tile.value != -1:
                    tile.value = -1
                    break

        self.minesweeper.put_right_numbers()


    def check_map(self) -> bool:
        """
        Checks tile map if theres no mine at start pos , if no guessing mode then checks for 0 tile at start and neighbor 0 tiles 
        """
        
        if self.start_pos:
            start_tile = self.minesweeper.get_tile(*self.start_pos)

            if start_tile.value == -1:
                    
                    return False
                    
            
            if self.no_guess:
                if start_tile.value != 0 or len(self.minesweeper.get_neighbors_with_value(start_tile,0)) == 0:
                    return False

        
        return True

    def generate_needed_map(self) -> bool:
        if self.start_pos == None:
            return False
        
        solver = Solver(self.start_pos)
        i=0
        while self.check_map() == False or (self.no_guess == True and solver.solve(deepcopy(self.minesweeper.map_data))==False ):
                
            i+=1
            if i > 1000:
                return False
            
            print('creating new map')
            self.generate_tile_map()

        return True

class Solver:
    """
    Bot for solving minesweeper boards and checking if they dont need guesses.
    """

    def __init__(self,start_pos:tuple):
        self.start_pos = start_pos
        self.game = None

    def solve(self,tile_map:TILE_MAP) -> bool:
        self.game = Minesweeper(tile_map)
        self.game.start_game()
        
        while True:
            decisions = self.get_logic_decisions()

            if not decisions:
                break

            for dec in decisions:
                
                dig,tile = dec

                if dig == True:
                    result,_ = self.game.recursive_reveal(tile)
                    
                    if result == 'win':
                        return True
                    elif result == 'lose':
                        return False
                else:
                    self.game.flag_tile(tile)
        return False

    def get_logic_decisions(self) -> list[tuple[bool,Tile]]:
        
        start_tile = self.game.get_tile(*self.start_pos)
        if start_tile.revealed == False:
            if start_tile.value != -1:
                return [(True,start_tile)]
            else:
                return None
        
        decisions = []
        
        for n_tile in self.game._get_revealed_tiles():
            neighbors = self.game.get_neighbor_tiles(n_tile)
            neighbor_flagged_mines:list[Tile] = []
            neighbor_unrevealed_tiles:list[Tile] = []
            
            for neighbor in neighbors:
                if neighbor.flagged == True:
                    neighbor_flagged_mines.append(neighbor)
                if neighbor.revealed == False:
                    neighbor_unrevealed_tiles.append(neighbor)
            
            dig = None
            if n_tile.value == len(neighbor_flagged_mines):
                dig = True    
            elif n_tile.value == len(neighbor_unrevealed_tiles):
                dig = False
            
            if dig is not None:
                 for n_neighbor in neighbor_unrevealed_tiles:
                    if not ((dig,n_neighbor) in decisions) and n_neighbor.flagged == False and n_neighbor.revealed == False:
                        decisions.append((dig,n_neighbor))
                    
        
        return decisions

            
            