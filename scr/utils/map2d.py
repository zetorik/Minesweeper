class MapObject:
    """
    Basic class for creating objects with a value in 2D maps
    """

    def __init__(self,value,row:int,column:int) -> None:
        self.value = value
        self.row = row
        self.column = column

    def get_pos(self) -> tuple :
        return self.row, self.column
    
map2d = list[list[MapObject]]

class Map2DGeneration:
    """
    Basic class for generating 2D maps
    """
    def __init__(self,width:int,height:int) -> None:
        self.width = width
        self.height = height
        self.map_data = None
    
    def generate_map(self,value:any =0) -> map2d:
        self.map_data = [[MapObject(value,r,c) for c in range(self.width)] for r in range(self.height)]
        return self.map_data
    
class Map2D:
    """
    Basic class for doing things with 2D maps
    """
    
    def __init__(self,map_data:map2d=None) -> None:
        if map_data != None:
            self.set_map_data(map_data)
        else:
            self.map_data = None
    
    def set_map_data(self,map_data:map2d):
        self.map_data = map_data
        self.width = len(map_data[0])
        self.height = len(map_data)

    
    def print(self) -> None:
        for row in self.map_data:
            for tile in row:
                print( tile.value,end='')
            print()
        print(' ')


    def get_object(self,row:int,column:int) -> MapObject:
        return self.map_data[row][column]
    
    def get_neighbor_objects(self,obj:MapObject) -> list[MapObject]:
        objs = []
        row,column = obj.get_pos()
        
        for dr,dc in [ (0,-1),  (0,1), (-1,0), (-1,-1), (-1,1), (1,0), (1,-1), (1,1) ]:
            if 0 <= row+dr <= self.height-1 and 0<= column+dc <= self.width-1:
                objs.append(self.get_object(row+dr,column+dc))
        return objs
    
    def get_all_objects(self) -> list:
        return [obj for row in self.map_data for obj in row ]
    
    def get_distance(self,obj1:MapObject,obj2:MapObject) -> int:
        return abs(obj1.row - obj2.row) + abs(obj1.column - obj2.column)