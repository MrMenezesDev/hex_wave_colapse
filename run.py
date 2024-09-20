import py5

from hex_grid import HexGrid
from hex_wave_collapse import HexWaveFunctionCollapseGrid, Tile, Cell

hex_grid = None

def settings():
    py5.size(1024, 1024)  # Defina o tamanho da tela
    
def setup():
    global hex_grid
    dim = 5
    grid = HexGrid(cols=dim, rows=dim, size=100, py5=py5)
    grid.draw()
    hex_grid = HexWaveFunctionCollapseGrid(dim=dim, draw_cell=grid.draw_cell, border=True)
    hex_grid.start()
    print("started!")

def draw():
    global hex_grid
    hex_grid.collapse()
    hex_grid.draw()
    if hex_grid.complete:
        print("finished!")
        py5.no_loop()

py5.run_sketch()