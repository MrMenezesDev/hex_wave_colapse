import py5

from hex_grid import Grid
from hex_wave_collapse import HexWaveFunctionCollapseGrid, Tile

hex_grid = None

def settings():
    py5.size(600, 600)  # Defina o tamanho da tela
    
def setup():
    global hex_grid
    dim = 4
    grid = Grid(cols=dim, rows=dim, size=75, py5=py5)
    grid.draw()
    tile1 = Tile(edges=[1, 1, 0, 0, 0, 0]) # 0,0
    tile2 = Tile(edges=[0, 0, 1, 1, 0, 0]) # 0,1
    tile3 = Tile(edges=[0, 0, 0, 0, 1, 1]) # 1,0
    tile4 = Tile(edges=[0, 0, 0, 0, 0, 0]) # 1,1
    # tile5 = Tile(edges=[1, 0, 0, 0, 1, 1]) # 1,1
    # tile6 = Tile(edges=[1, 1, 0, 0, 0, 1]) # 1,1

    tiles=[tile1, tile2, tile3, tile4]#, tile5, tile6]
    hex_grid = HexWaveFunctionCollapseGrid(dim=dim, tiles=tiles, draw_cell=grid.draw_cell)
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