# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pygame",
# ]
# ///
import pygame
from hex_grid import HexGrid
from hex_wave_collapse import HexWaveFunctionCollapseGrid, Tile, Cell

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da tela
screen = pygame.display.set_mode((512 + 256, 512))

hex_grid = None

def setup():
    global hex_grid
    col = 10
    row = 5
    grid = HexGrid(cols=col, rows=row, size=50, draw_vertex=draw_vertex, draw_map=draw_map)
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

def draw_vertex(vertexs, color):
    pygame.draw.polygon(screen, color, vertexs)

def draw_map(vertexs, color):
    pygame.draw.polygon(screen, color, vertexs, 1)

def draw_button(screen, x, y, w, h, text):
    pygame.draw.rect(screen, (200, 0, 0), (x, y, w, h))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + 10, y + 10))

def is_button_clicked(x, y, w, h, mouse_pos):
    return x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h

# Loop principal
setup()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_button_clicked(10, 10, 100, 50, event.pos):
                running = False

    screen.fill((255, 255, 255))  # Limpa a tela com a cor branca
    draw()
    draw_button(screen, 10, 10, 100, 50, "Fechar")
    pygame.display.flip()  # Atualiza a tela

pygame.quit()
exit()