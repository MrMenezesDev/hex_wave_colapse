# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "py5",
#     "numpy",
# ]
# ///

import time
import math
import threading

import py5
import numpy as np

class HexGrid:
    """
    Esta classe representa um grid de tiles desenhados na tela.
    """

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
        """
        Desenha o grid de hexágonos na tela.
        """
        for y in range(self.rows):
            for x in range(self.cols):
                offset_y = self.hex_height / 2 if x % 2 == 1 else 0
                center_x = x * self.hex_width + self.offset
                center_y = y * self.hex_height + offset_y + self.offset
                color = 0 if self.state[y, x] == 1 else 255
                self.draw_hexagon(center_x, center_y, self.size, color)

    def draw_hexagon(self, x, y, size, color):
        """
        Desenha um hexágono na posição (x, y) com o tamanho e cor especificados.
        """
        vertices = []
        for i in range(6):
            angle = (math.pi * 2 / 6 * i)
            vx = x + math.cos(angle) * size
            vy = y + math.sin(angle) * size
            vertices.append((vx, vy))

        self.draw_map(vertices, color)

def draw_map(vertices, color):
    """
    Desenha o mapa de hexágonos.
    """
    py5.fill(color)
    py5.begin_shape()
    for vx, vy in vertices:
        py5.vertex(vx, vy)
    py5.end_shape(py5.CLOSE)

def draw_vertex(vertices, color):
    """
    Desenha os vértices dos hexágonos.
    """
    py5.stroke(color)
    py5.begin_shape()
    for vx, vy in vertices:
        py5.vertex(vx, vy)
    py5.end_shape(py5.CLOSE)

def apply_rule(rule, state, x, y):
    """
    Aplica a regra de evolução celular para a célula na posição (x, y).
    """
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

def evolve(rule, initial_state, steps, temp=False):
    """
    Evolui o estado inicial das células por um número de passos, aplicando a regra especificada.
    """
    start_time = time.time()
    state = initial_state.copy()
    history = [state.copy()]
    
    for step in range(steps):
        new_state = np.zeros_like(state)
        for x in range(state.shape[0]):
            for y in range(state.shape[1]):
                new_state[x, y] = apply_rule(rule, state, x, y)
        state = new_state
        history.append(state.copy())
        time.sleep(0.02)  # Adiciona um pequeno intervalo de descanso
    
    end_time = time.time()
    print(f"evolve function took {end_time - start_time:.4f} seconds")
    if temp:
        global temp_evolution_history
        temp_evolution_history = history
    else:
        return history

def settings():
    """
    Configura o tamanho da janela.
    """
    py5.size(800, 800)

def setup():
    """
    Configura o ambiente inicial do sketch.
    """
    global hex_grid, evolution_history, step, direction
    start_time = time.time()
    py5.background(255)
    step = 0
    direction = 1
    hex_grid = HexGrid(50, 50, 10, draw_vertex, draw_map)  # Inicialize hex_grid aqui
    end_time = time.time()
    print(f"setup function took {end_time - start_time:.4f} seconds")

def draw():
    """
    Função de desenho chamada repetidamente pelo py5.
    """
    start_time = time.time()
    global step, direction, evolution_history
    py5.background(255)
    if evolution_history:
        hex_grid.set_state(evolution_history, step)
        hex_grid.draw()
        step += direction
        if step == len(evolution_history) - 1:
            direction = -1
            print("Starting evolution in a separate thread")
            start(update=False)
        elif step == 0:
            direction = 1
            plot_evolution_temp()
    end_time = time.time()
    print(f"draw function took {end_time - start_time:.4f} seconds")

def plot_evolution(hist):
    """
    Atualiza a evolução histórica e reinicia o passo e a direção.
    """
    global evolution_history, step, direction
    evolution_history = hist
    step = 0
    direction = 1

def plot_evolution_temp():
    """
    Atualiza a evolução histórica temporária e reinicia o passo e a direção.
    """
    global temp_evolution_history, step, direction, evolution_history
    evolution_history = temp_evolution_history
    step = 0
    direction = 1

def start(update=True,steps=50):
    """
    Inicia a evolução das células, possivelmente em uma thread separada.
    """
    start_time = time.time()
    global hex_grid, step, direction, temp_evolution_history
    rule = np.random.randint(0, 2, size=256)  # Defina sua regra de 8 vizinhos aqui

    initial_state = np.zeros((steps, steps), dtype=int)
    initial_state[25, 25] = 1  # Estado inicial

    def generate_evolution():
        print("Evolution thread started")
        evolve(rule, initial_state, steps, temp=True)
        print("Evolution thread finished")

    if update:
        ev_history = evolve(rule, initial_state, steps)
        plot_evolution(ev_history)
    else:
        threading.Thread(target=generate_evolution).start()
    
    end_time = time.time()
    print(f"start function took {end_time - start_time:.4f} seconds")

# Variáveis globais
hex_grid = None
evolution_history = None
temp_evolution_history = None
step = 0
direction = 1

# Inicia o sketch
start()
py5.run_sketch()