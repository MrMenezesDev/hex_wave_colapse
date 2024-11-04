# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "py5",
#     "numpy",
# ]
# ///
import numpy as np
import py5
from dataclasses import field
import math

class HexGrid:
    """
    Esta classe representa um grid de tiles desenhados na tela.
    """

    col: int
    row: int
    size: int
    cells: list = field(default_factory=list)

    def __init__(self, cols, rows, size, draw_vertex, draw_map, colors=["#666666", "#999999", "#333333"]):
        self.cols = cols
        self.rows = rows
        self.size = size
        self.draw_vertex = draw_vertex
        self.draw_map = draw_map
        self.colors = colors
        self.hex_height = math.sin(math.pi * 2 / 6) * size * 2  # Altura do hexágono
        self.hex_width = size * 1.5  # Largura do hexágono
        self.offset = size
        self.state = np.zeros((rows, cols), dtype=int)  # Estado inicial das células

    def set_state(self, evolution_history, step):
        """
        Define o estado das células com base no evolution_history e no passo atual.
        """
        self.state = evolution_history[step]

    def draw(self):
        for y in range(self.rows):
            for x in range(self.cols):
                offset_y = self.hex_height / 2 if x % 2 == 1 else 0
                center_x = x * self.hex_width + self.offset
                center_y = y * self.hex_height + offset_y + self.offset
                color = 0 if self.state[y, x] == 1 else 255
                self.draw_hexagon(center_x, center_y, self.size, color)

    def draw_hexagon(self, x, y, size, color):
        # Calcular os vértices do hexágono
        vertices = []
        for i in range(6):
            angle = (math.pi * 2 / 6 * i)
            vx = x + math.cos(angle) * size
            vy = y + math.sin(angle) * size
            vertices.append((vx, vy))

        # Desenhar o hexágono
        self.draw_map(vertices, color)

def draw_map(vertices, color):
    py5.fill(color)
    py5.begin_shape()
    for vx, vy in vertices:
        py5.vertex(vx, vy)
    py5.end_shape(py5.CLOSE)

def draw_vertex(vertices, color):
    py5.stroke(color)
    py5.begin_shape()
    for vx, vy in vertices:
        py5.vertex(vx, vy)
    py5.end_shape(py5.CLOSE)

def apply_rule(rule, state, x, y):
    neighbors = [
        state[(x - 1) % state.shape[0], (y - 1) % state.shape[1]],  # cima-esquerda
        state[(x - 1) % state.shape[0], y],                         # cima
        state[(x - 1) % state.shape[0], (y + 1) % state.shape[1]],  # cima-direita
        state[x, (y - 1) % state.shape[1]],                         # esquerda
        state[x, (y + 1) % state.shape[1]],                         # direita
        state[(x + 1) % state.shape[0], (y - 1) % state.shape[1]],  # baixo-esquerda
        state[(x + 1) % state.shape[0], y],                         # baixo
        state[(x + 1) % state.shape[0], (y + 1) % state.shape[1]]   # baixo-direita
    ]
    index = sum([2**i * neighbors[i] for i in range(8)])
    return rule[index]

def evolve(rule, initial_state, steps):
    state = initial_state.copy()
    history = [state.copy()]
    
    for step in range(steps):
        new_state = np.zeros_like(state)
        for x in range(state.shape[0]):
            for y in range(state.shape[1]):
                new_state[x, y] = apply_rule(rule, state, x, y)
        state = new_state
        history.append(state.copy())
    
    return history

def setup():
    global hex_grid, evolution_history, step, direction
    py5.size(800, 800)
    py5.background(255)
    step = 0
    direction = 1

def draw():
    global step, direction
    py5.background(255)
    hex_grid.set_state(evolution_history, step)
    hex_grid.draw()
    step += direction
    if step == len(evolution_history) - 1:
        direction = -1
    elif step == 0:
        direction = 1
        start()

def plot_evolution(hist):
    global evolution_history, step, direction
    evolution_history = hist
    step = 0
    direction = 1

# Exemplo de uso

def start():
    global hex_grid, evolution_history, step, direction
    rule = np.random.randint(0, 2, size=256)  # Defina sua regra de 8 vizinhos aqui

    initial_state = np.zeros((50, 50), dtype=int)
    initial_state[25, 25] = 1  # Estado inicial
    steps = 50
    evolution_history = evolve(rule, initial_state, steps)

    # Inicialize o HexGrid
    hex_grid = HexGrid(50, 50, 10, draw_vertex, draw_map)

    plot_evolution(evolution_history)

hex_grid = None
evolution_history = None
step = 0
direction = 1
start()
py5.run_sketch()