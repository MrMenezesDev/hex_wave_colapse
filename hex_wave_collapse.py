from dataclasses import dataclass, field
import random

@dataclass
class Tile:
    """
    Esta classe representa uma imagem de tile do py5 com suas bordas de possíveis conexões.
    A lista de bordas (edges) representa os tipos possíveis de conexão entre este tile e seus vizinhos.
    A posição da conexão na lista de bordas indica a orientação delas.
    """
    edges: list
    
    def get_side(self, side):
        return self.edges[side]

@dataclass
class Cell:
    col: int
    row: int
    options: list
    tile: Tile = field(default=None, init=False)  
    
    def __init__(self, col, row, options=[], tile=None):
        self.col = col
        self.row = row
        self.options = options
        self.tile = tile
    @property
    def collapsed(self):
        return self.tile is not None

    def collapse(self):
        self.tile = random.choice(self.options)

    @property
    def entropy(self):
        if self.collapsed:
            return 0
        return len(self.options)
        
    def update_options(self, collapsed_cell):
        # self = 1,1
        # collapsed_cell = 0,1
        ref_tile = collapsed_cell.tile
        if self.col == collapsed_cell.col:
            if self.row > collapsed_cell.row:
                cond = lambda tile: tile.get_side(0) == ref_tile.get_side(3)
            else:
                cond = lambda tile: tile.get_side(3) == ref_tile.get_side(0)
        elif self.row == collapsed_cell.row:
            if self.col > collapsed_cell.col:
                cond = lambda tile: tile.get_side(5) == ref_tile.get_side(2)
            else:
                cond = lambda tile: tile.get_side(1) == ref_tile.get_side(4)
        else:
            if self.col > collapsed_cell.col:
                if self.row < collapsed_cell.row:
                    cond = lambda tile: tile.get_side(4) == ref_tile.get_side(1)
                else:
                    cond = lambda tile: tile.get_side(5) == ref_tile.get_side(2)
            elif self.row > collapsed_cell.row:
                cond = lambda tile: tile.get_side(1) == ref_tile.get_side(4)
            else:
                cond = lambda tile: tile.get_side(2) == ref_tile.get_side(5)
        self.options = list(filter(cond, self.options))

