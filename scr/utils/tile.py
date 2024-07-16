from .map2d import MapObject

class Tile(MapObject):
    """
    Represents a tile in the Minesweeper map
    """
    
    def __init__(self,value:int,row:int,column:int,revealed:bool=False,flagged:bool=False,hinted:bool=False) :
        super().__init__(value,row,column)
        
        self.revealed = revealed
        self.flagged = flagged
        self.hinted =hinted

