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

    def __init__(self, cols, rows, size, draw_vertex,draw_map, colors=["#666666", "#999999", "#333333"]):
        self.cols = cols
        self.rows = rows
        self.size = size
        self.draw_vertex = draw_vertex
        self.draw_map = draw_map
        self.colors = colors
        self.hex_height = math.sin(math.pi * 2 / 6) * size * 2  # Altura do hexágono
        self.hex_width = size * 1.5  # Largura do hexágono
        self.offset = size

    def draw(self):
        for y in range(self.rows):
            for x in range(self.cols):
                offset_y = self.hex_height / 2 if x % 2 == 1 else 0
                center_x = x * self.hex_width + self.offset
                center_y = y * self.hex_height + offset_y + self.offset
                self.draw_hexagon(center_x, center_y, self.size)
                self.draw_hexagon(
                    center_x, center_y, self.size * 0.29, math.pi * 2 / 12, self.colors
                )

    def draw_cell(self, cell):
        """
        Este método desenha um caminho do centro do hexágono até a borda do hexágono.
        O caminho é desenhado apenas se a célula estiver colapsada.
        Pode ser desenhadas 0 a 6 linhas, sendo elas 0 o topo.
        Cada edge representa uma direção e o valor 1 indica que a borda está conectada.
        """
        if not cell.collapsed:
            return

        # Centro do hexágono
        center_x = cell.col * self.hex_width + self.offset
        center_y = (
            cell.row * self.hex_height
            + (self.hex_height / 2 if cell.col % 2 == 1 else 0)
            + self.offset
        )

        # Tamanho do hexágono
        size = self.size
        # colors = ["#999999", "#666666", "#333333"]

        for i in [3, 5, 1, 2, 4, 0]:
            edge = cell.tile.edges[i]
            index = [4, -1, 0, 1, 2, 3][i]
            if edge == 1:
                # Calcular os ângulos dos dois vértices que formam a borda
                angle1 = math.pi * 2 / 6 * index
                angle2 = math.pi * 2 / 6 * ((index + 1) % 6)

                # Calcular a posição dos dois vértices
                vertex1_x = center_x + math.cos(angle1) * size
                vertex1_y = center_y + math.sin(angle1) * size
                vertex2_x = center_x + math.cos(angle2) * size
                vertex2_y = center_y + math.sin(angle2) * size

                # Calcular a posição do ponto médio da borda
                edge_x = (vertex1_x + vertex2_x) / 2
                edge_y = (vertex1_y + vertex2_y) / 2

                # Definir as cores das linhas
                color = [[0, 5, 8, 9], [3, 4, 6, 7], [1, 2, 10, 11]]
                c1 = (
                    self.colors[2]
                    if (i + 6) in color[0]
                    else self.colors[0] if (i + 6) in color[1] else self.colors[1]
                )
                c2 = (
                    self.colors[2]
                    if i in color[0]
                    else self.colors[0] if i in color[1] else self.colors[1]
                )

                # Draw parallel lines
                self.draw_parallel_shapes(center_x, center_y, edge_x, edge_y, [c1, c2])

        return (f"{cell.col},{cell.row}", center_x, center_y)

    def draw_parallel_shapes(self, x, y, x1, y1, colors, angle=30, factor=-1):
        # Calcular o vetor perpendicular
        dx = x1 - x
        dy = y1 - y
        length = (dx**2 + dy**2) ** 0.5
        perp_x = -dy / length * self.size / 4
        perp_y = dx / length * self.size / 4

        # Calcular as novas posições para as linhas paralelas
        x2, y2 = x + perp_x, y + perp_y
        x3, y3 = x1 + perp_x, y1 + perp_y
        x4, y4 = x - perp_x, y - perp_y
        x5, y5 = x1 - perp_x, y1 - perp_y

        xi, yi = line_intersection(
            x, y, *get_rotation_in_line(x, y, x2, y2, angle * factor), x3, y3, x2, y2
        )

        # Desenhar a linha principal
        vertex_initial = [(x, y), (x1, y1), (x3, y3), (xi, yi)]

        self.draw_vertex(vertex_initial, colors[0])

        xin, yin = line_intersection(
            x, y, *get_rotation_in_line(x, y, x4, y4, -angle * factor), x5, y5, x4, y4
        )

        # Desenhar a forma paralela
        vertex_parallel = [(x, y), (x1, y1), (x5, y5), (xin, yin)]
        self.draw_vertex(vertex_parallel, colors[1])
        
    def draw_hexagon(self, x, y, size, rotation=0, colors=None):
        # Calcular os vértices do hexágono
        vertices = []
        for i in range(6):
            angle = (math.pi * 2 / 6 * i) + rotation
            vx = x + math.cos(angle) * size
            vy = y + math.sin(angle) * size
            vertices.append((vx, vy))

        # Desenhar os losângulos
        if colors and len(colors) >= 3:
            for i in [-2, 0, 2]:
                self.draw_vertex([
                    (x, y),
                    (vertices[i - 1][0], vertices[i - 1][1]),
                    (vertices[i][0], vertices[i][1]),
                    (vertices[i + 1][0], vertices[i + 1][1]),
                ], colors[i])
        else:
            self.draw_map(vertices, 255)
            
        return vertices
       

def get_rotation_in_line(x1, y1, x2, y2, angle):
    import math

    # Vetor AB (de A para B)
    AB_x = x2 - x1
    AB_y = y2 - y1

    # Ângulo de rotação (30 graus convertidos para radianos)
    angulo_radianos = math.radians(angle)

    # Matriz de rotação
    cos_theta = math.cos(angulo_radianos)
    sin_theta = math.sin(angulo_radianos)

    # Vetor AC (rotacionado)
    AC_x = cos_theta * AB_x - sin_theta * AB_y
    AC_y = sin_theta * AB_x + cos_theta * AB_y

    # Coordenadas do ponto C
    x_C = x1 + AC_x
    y_C = y1 + AC_y

    return x_C, y_C


def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  # Linhas são paralelas
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
    return px, py
