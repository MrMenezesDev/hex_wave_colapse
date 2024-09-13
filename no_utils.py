import py5

def draw_parallel_lines(self, x, y, x1, y1, distance, colors):
    distance = distance / 2
    # Calcular o vetor perpendicular
    dx = x1 - x
    dy = y1 - y
    length = (dx**2 + dy**2)**0.5
    perp_x = -dy / length * distance
    perp_y = dx / length * distance

    # Calcular as novas posições para as linhas paralelas
    x2, y2 = x + perp_x, y + perp_y
    x3, y3 = x1 + perp_x, y1 + perp_y
    x4, y4 = x - perp_x, y - perp_y
    x5, y5 = x1 - perp_x, y1 - perp_y

    # Desenhar a linha principal
    py5.line(x, y, x1, y1)

    # Desenhar as linhas paralelas
    
    py5.stroke(colors[0])
    py5.line(x2, y2, x3, y3)
    py5.stroke(colors[1])
    py5.line(x4, y4, x5, y5)
