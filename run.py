# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "py5",
# ]
# ///

import py5

from hex_grid import HexGrid
from hex_wave_collapse import HexWaveFunctionCollapseGrid, Tile, Cell

hex_grid = None


def settings():
    py5.size(512 + 256, 512)  # Defina o tamanho da tela


def setup():
    global hex_grid
    col = 10
    row = 5
    grid = HexGrid(cols=col, rows=row, size=50, draw_vertex=draw_vertex, draw_map=draw_map)
    grid.draw()
    hex_grid = HexWaveFunctionCollapseGrid(
        dim=[col, row], draw_cell=grid.draw_cell, border=True
    )
    hex_grid.start()
    print("started!")


def draw():
    global hex_grid
    hex_grid.collapse()
    hex_grid.draw()
    if hex_grid.complete:
        print("finished!")
        py5.no_loop()


def draw_vertex(vertexs, color):
    py5.no_stroke()
    py5.begin_shape()
    py5.fill(color)
    for x, y in vertexs:
        py5.vertex(x, y)
    py5.end_shape(py5.CLOSE),


def draw_map(vertexs, color):
    py5.begin_shape()
    py5.stroke(0)
    py5.stroke_weight(1)
    py5.fill(color)
    for vx, vy in vertexs:
        py5.vertex(vx, vy)
    py5.end_shape(py5.CLOSE)


py5.run_sketch()

