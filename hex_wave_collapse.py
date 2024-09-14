from dataclasses import dataclass, field
from functools import cached_property
from itertools import product
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
    dim: int
    options: list
    tile: Tile = field(default=None, init=False)  
    
    def __init__(self, col, row, dim, options=[], tile=None, border=False):
        self.col = col
        self.row = row
        self.options = options
        self.tile = tile
        self.dim = dim
        if border:
            self.update_border_options()

    @property
    def collapsed(self):
        return self.tile is not None

    def collapse(self):
        self.tile = random.choice(self.options)
        print(f"Tile {self.col},{self.row} collapsed to {self.tile.edges}")
        print(f"Options: {len(self.options)}")

    @property
    def entropy(self):
        if self.collapsed:
            return 0
        return len(self.options)
   
    def update_border_options(self):
        if self.col == 0:
            self.options = [tile for tile in self.options if tile.get_side(4) == 0 or tile.get_side(5) == 0]
        if self.row == 0:
            self.options = [tile for tile in self.options if tile.get_side(0) == 0]
        if self.row == self.dim - 1:
            self.options = [tile for tile in self.options if tile.get_side(1) == 0 or tile.get_side(2) == 0]
        if self.col == self.dim - 1:
            self.options = [tile for tile in self.options if tile.get_side(3) == 0]
    
    def update_options(self, collapsed_cell):
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

@dataclass
class HexWaveFunctionCollapseGrid:
    """
    Classe WaveFunctionCollapseGrid
    ===============================
    Classe para representar uma grade que será populada colapsando suas células.
    Atributos:
    ----------
    tiles : list
        Lista de tiles disponíveis para a grade.
    dim : int
        Dimensão da grade.
    pending_cells : list[Cell]
        Lista de células pendentes que ainda não foram colapsadas.
    Métodos:
    --------
    __post_init__():
        Inicializa a lista de células pendentes com uma cópia das células e embaralha a lista.
    w():
        Retorna a largura de cada célula na grade.
    h():
        Retorna a altura de cada célula na grade.
    cells():
        Retorna uma lista de células inicializadas com todas as tiles possíveis.
    start():
        Inicia o algoritmo escolhendo uma célula aleatória e colapsando-a.
    collapse_cell(cell):
        Colapsa a célula especificada, remove-a da lista de células pendentes e atualiza as opções das células vizinhas.
    get_neighbors(cell):
        Dada uma célula, retorna a lista de vizinhos que ainda não foram colapsados.
    complete():
        Retorna True se todas as células foram colapsadas, caso contrário, False.
    collapse():
        Obtém a próxima célula pendente com a menor entropia e a colapsa.
    draw():
        Desenha a grade, exibindo as imagens das células colapsadas.
    Class to represent a grid which will be populated by collapsing their cells.
    """

    tiles: list
    dim: int
    pending_cells: list[Cell] = field(default=list, init=False)
    draw_cell: callable
    border: bool = False
    
    def __post_init__(self):
        self.pending_cells = self.cells[:]  # copy of cells, so we can know which aren't collapsed
        random.shuffle(self.pending_cells)

    @cached_property
    def cells(self):
        return [
            Cell(col=i, row=j, dim=self.dim, options=self.tiles[:], border=self.border)  # cells initialized with all tiles as possibles
            for i, j in product(range(0, self.dim), range(0, self.dim))
        ]

    def start(self):
        """
        To start the algorithm, we pick any random cell and collapse it since all of them have the
        same set of possible tiles.
        """
        cell = random.choice(self.cells)
        self.collapse_cell(cell)

    def collapse_cell(self, cell: Cell):
        # defines the cell tile among their options
        cell.collapse()
        # remove the collapsed cell from the pending ones list
        self.pending_cells.remove(cell)
        # update all the neighbors cells options considering the collapse operation
        for neighbor_cell in self.get_neighbors(cell):
            neighbor_cell.update_options(collapsed_cell=cell)

    def get_neighbors(self, cell: Cell):
        """
        Given a cell, return its list of neighbors which still weren't collapsed.
        """
        i, j = cell.col, cell.row
        positions = [
            (i, j - 1),
            (i + 1, j + 1),
            (i, j + 1),
            (i + 1, j),
            (i - 1, j),
            (i - 1, j + 1),
        ]

        #       1,0  
        # 0,1 - 1,1 - 2,1
        # 0,2 - 1,2 - 2,2
        
        return [
            c for c in self.pending_cells if all(((c.col == i or c.row == j), (c.col, c.row) in positions))
        ]

    @property
    def complete(self):
        return not self.pending_cells

    def collapse(self):
        """
        Gets the next pending cell with the lowes entropy and collapses it
        """
        next_cell = sorted(self.pending_cells, key=lambda c: c.entropy)[0]
        self.collapse_cell(next_cell)

    def draw(self):
        for cell in self.cells:
            if cell.collapsed:
                self.draw_cell(cell)
                pass# py5.image(cell.tile.image, cell.i * self.w, cell.j * self.h, self.w, self.h)
            