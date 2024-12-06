import math
import py5

from hex_grid import HexGrid
from utils_py5 import draw_map, draw_vertex
from hex_wave_collapse import Cell, Tile

grid = None

def settings():
    py5.size(1024, 1024)  # Defina o tamanho da tela

def passo(a,b):
    pass
def setup():
    global grid
    col = 4
    row = 3
    size = 150  # Tamanho do hexágono
    central_cube_size = 0.5
    bar_thickness = 0.4*0.3
    colors = ["#FFFF00", "#CCCC00", "#999900"]  # Amarelo e seus contrastes
    color_bars = ["#FFA07A", "#E9967A","#FA8072" ]  # Vermelho alaranjado e seus contrastes
    color_bars =  ["#F96F00", "#F93C00", "#F90900"] 
    grid = HexGrid(cols=col, rows=row, size=size, draw_vertex=draw_vertex, draw_map=passo, central_cube_size=central_cube_size, bar_thickness=bar_thickness, colors=colors, color_bars=color_bars)
    grid.draw()
    # Configuração inicial para os testes
    tile1 = Tile(edges=[1, -1, 1, 1, -1, -1]) # -1,-1
    tile2 = Tile(edges=[1, 1, -1, 1, -1, -1]) # -1,1
    tile3 = Tile(edges=[-1, -1, -1, -1, 1, 1]) # 1,-1
    tile4 = Tile(edges=[-1, -1, -1, -1, -1, -1]) # 1,1
    tile5 = Tile(edges=[1, 1, 1, -1, -1, -1]) # 1,1
    tile6 = Tile(edges=[1, -1, -1, -1, -1, 1]) # 1,1
    tile7 = Tile(edges=[-1, -1, -1, 1, 1, -1]) # 1,1

    cell00 = Cell(col=0, row=0, grid_dimensions=[col, row])
    cell01 = Cell(col=0, row=1, grid_dimensions=[col, row])
    cell10 = Cell(col=1, row=0, grid_dimensions=[col, row])
    cell11 = Cell(col=1, row=1, grid_dimensions=[col, row])
    cell21 = Cell(col=2, row=1, grid_dimensions=[col, row])
    cell22 = Cell(col=2, row=2, grid_dimensions=[col, row])
    cell12 = Cell(col=1, row=2, grid_dimensions=[col, row])
    cell02 = Cell(col=0, row=2, grid_dimensions=[col, row])
    cell20 = Cell(col=2, row=0, grid_dimensions=[col, row])
    
    cell31 = Cell(col=3, row=1, grid_dimensions=[col, row])
    cell32 = Cell(col=3, row=2, grid_dimensions=[col, row])
    cell30 = Cell(col=3, row=0, grid_dimensions=[col, row])
    
    cell00.set_edges([-1,-1,1,1,-1,-1])
    cell01.tile=tile2 
    cell10.set_edges([-1, 1, -1, -1, 1, 1])
    
    cell02.tile=tile5 
    cell12.tile=tile6 
    cell11.tile=tile7 
    
    cell21.tile=tile1 
    cell22.set_edges([1,1,-1,-1,-1,-1])
    cell31.set_edges([1,-1,-1,1,1,1])
    
    cell30.set_edges([-1, -1, -1, 1, -1, -1])
    cell20.set_edges([-1,-1,-1,1,1,-1])
    cell32.set_edges([1, -1, -1, -1, -1, -1])
    
    cells = [cell00, cell01, cell10, cell11, cell21, cell22, cell12, cell02, cell20,cell31,cell30,cell32]
    
    grid.cells = cells

    for cell in cells:
        grid.draw_cell(cell)




py5.run_sketch()

