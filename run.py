import py5

from hex_grid import Grid
from hex_wave_collapse import Tile, Cell

def settings():
    py5.size(600, 600)  # Defina o tamanho da tela
    
def setup():
    dim = 5
    grid = Grid(cols=dim, rows=dim, size=75, py5=py5)
    grid.draw()
    tile1 = Tile(edges=[0, 0, 1, 1, 0, 0]) # 0,0
    tile2 = Tile(edges=[1, 1, 1, 0, 0, 0]) # 0,1
    tile3 = Tile(edges=[0, 0, 0, 1, 1, 1]) # 1,0
    tile4 = Tile(edges=[1, 0, 0, 0, 0, 1]) # 1,1
    
    options=[tile1, tile2, tile3, tile4]

    cell00 = Cell(col=0, row=0, tile=tile1)
    cell01 = Cell(col=0, row=1, tile=tile2)
    cell10 = Cell(col=1, row=0, tile=tile3)
    cell11 = Cell(col=1, row=1, tile=tile4)
    # grid.draw_cell(cell00)
    for cell in [cell00, cell01, cell10, cell11]:
        grid.draw_cell(cell)


py5.run_sketch()