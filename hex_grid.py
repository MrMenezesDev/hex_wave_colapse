import math
from dataclasses import dataclass, field
from typing import List, Callable, Tuple
from hex_wave_collapse import State
from math_utils import get_rotation_in_line, line_intersection

@dataclass
class HexGrid:
    cols: int
    rows: int
    size: float
    draw_vertex: Callable
    draw_map: Callable
    colors: List[str] = field(default_factory=lambda: ["#666666", "#999999", "#333333"])
    color_bars: List[str] = field(default_factory=lambda:  ["#666666", "#999999", "#333333"])
    cells: List = field(default_factory=list)
    hex_height: float = field(init=False)
    hex_width: float = field(init=False)
    offset: float = field(init=False)
    state: List[List[int]] = field(default_factory=list)
    central_cube_size: float = 0.3
    bar_thickness: float = 0.3

    def __post_init__(self):
        self.hex_height = math.sin(math.pi * 2 / 6) * self.size * 2  # Altura do hexágono
        self.hex_width = self.size * 1.5  # Largura do hexágono
        self.offset = self.size
        self.state = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
    
    def set_state(self, evolution_history, step):
        """
        Define o estado das células com base no evolution_history e no passo atual.
        """
        self.state = evolution_history[step]


    def calculate_center(self, col: int, row: int) -> Tuple[float, float]:
        """
        Calcula o centro do hexágono baseado na coluna e linha.
        """
        offset_y = self.hex_height / 2 if col % 2 == 1 else 0
        center_x = col * self.hex_width + self.offset
        center_y = row * self.hex_height + offset_y + self.offset
        return center_x, center_y

    def draw(self):
        for y in range(self.rows):
            for x in range(self.cols):
                center_x, center_y = self.calculate_center(x, y)
                if self.state[y][x] == 1:
                    self.draw_hexagon(center_x, center_y, self.size, color=1)
                else:
                    self.draw_hexagon(center_x, center_y, self.size)
                    # Desenhar um hexágono menor no centro
                    self.draw_hexagon(center_x, center_y, self.size * self.central_cube_size, math.pi * 2 / 12, self.colors)

    # Adicione os parâmetros bar_thickness e central_cube_size
    def draw_cell(self, cell):
        if not cell.collapsed:
            return

        center_x, center_y = self.calculate_center(cell.col, cell.row)
        size = self.size

        for i in [3, 5, 1, 2, 4, 0]:
            edge = cell.tile.edges[i]
            index = [4, -1, 0, 1, 2, 3][i]
            angle1 = math.pi * 2 / 6 * index
            angle2 = math.pi * 2 / 6 * ((index + 1) % 6)

            vertex1_x = center_x + math.cos(angle1) * size
            vertex1_y = center_y + math.sin(angle1) * size
            vertex2_x = center_x + math.cos(angle2) * size
            vertex2_y = center_y + math.sin(angle2) * size

            edge_x = (vertex1_x + vertex2_x) / 2
            edge_y = (vertex1_y + vertex2_y) / 2
            color = [[0, 5, 8, 9], [3, 4, 6, 7], [1, 2, 10, 11]]
            if edge == State.FILLED.value:
                c1 = (
                    self.color_bars[2]
                    if (i + 6) in color[0]
                    else self.color_bars[0] if (i + 6) in color[1] else self.color_bars[1]
                )
                c2 = (
                    self.color_bars[2]
                    if i in color[0]
                    else self.color_bars[0] if i in color[1] else self.color_bars[1]
                )
                self.draw_parallel_shapes(center_x, center_y, edge_x, edge_y, [c1, c2], impar=i % 2 > 0)
            elif edge == State.HOLE.value:
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
                self.draw_parallel_hole_shapes(center_x, center_y, edge_x, edge_y, [c1, c2])

        
    def find_fourth_point(self, A, B, C):
        # A, B, C são tuplas representando os pontos (x, y)
        # Calcule os vetores AB e AC
        AB = (B[0] - A[0], B[1] - A[1])
        AC = (C[0] - A[0], C[1] - A[1])
        
        # Calcule o ponto D
        D = (C[0] + AB[0], C[1] + AB[1])
        
        # Verifique se D é o ponto correto
        if (D[0] - B[0], D[1] - B[1]) == AC:
            return D
        else:
            # Se não, então o ponto D é (B[0] + AC[0], B[1] + AC[1])
            return (B[0] + AC[0], B[1] + AC[1])
        
    def draw_parallel_shapes(self, x, y, x1, y1, colors, angle=30, factor=-1, impar=False):
        x, y, x1, y1, perp_x, perp_y, bar_thickness = self.calculate_parallel_parameters(x, y, x1, y1, impar)
        
        x3, y3, x5, y5, xi, yi, xin, yin = self.calculate_intersections(x, y, x1, y1, perp_x, perp_y, angle, factor, impar)

        if impar:
            colors = colors[::-1]
        vertex_initial = [(x, y), (x1, y1), (x3, y3), (xi, yi)]
        self.draw_vertex(vertex_initial, colors[0])

        vertex_parallel = [(x, y), (x1, y1), (x5, y5), (xin, yin)]
        self.draw_vertex(vertex_parallel, colors[1])

    def draw_parallel_hole_shapes(self, x, y, x1, y1, colors, angle=30, factor=-1):
        x, y, x1, y1, perp_x, perp_y, bar_thickness = self.calculate_parallel_parameters(x, y, x1, y1)
        
        x3, y3, x5, y5, xi, yi, xin, yin = self.calculate_intersections(x, y, x1, y1, perp_x, perp_y, angle, factor)

        x1, y1 = self.find_fourth_point([x, y], [xin, yin], [xi, yi])

        vertex_initial = [(x, y), (x1, y1), (xi, yi)]
        self.draw_vertex(vertex_initial, colors[0])
        
        vertex_parallel = [(x, y), (x1, y1), (xin, yin)]
        self.draw_vertex(vertex_parallel, colors[1])

    def calculate_parallel_parameters(self, x, y, x1, y1, impar=False):
        recuo = (self.bar_thickness / self.central_cube_size)
        direction_x = x1 - x
        direction_y = y1 - y
        length = math.sqrt(direction_x**2 + direction_y**2)
        if length != 0:
            direction_x /= length
            direction_y /= length

        bar_thickness = self.size * (self.central_cube_size * math.sqrt(3) / 2) * recuo

        if impar:         
            x += ((direction_x * self.size * self.central_cube_size)) 
            y += ((direction_y * self.size * self.central_cube_size))
        else:
            x += ((direction_x * self.size * self.central_cube_size) / 2) - ((direction_x * bar_thickness) / 2)
            y += ((direction_y * self.size * self.central_cube_size) / 2) - ((direction_y * bar_thickness) / 2)

        perp_x = -direction_y * bar_thickness
        perp_y = direction_x * bar_thickness

        return x, y, x1, y1, perp_x, perp_y, bar_thickness

    def calculate_intersections(self, x, y, x1, y1, perp_x, perp_y, angle, factor, impar=False):
        if impar:
            x2, y2 = x - perp_x, y - perp_y 
            x3, y3 = x1 - perp_x, y1 - perp_y
            x4, y4 = x + perp_x, y + perp_y
            x5, y5 = x1 + perp_x, y1 + perp_y
        else:
            x2, y2 = x + perp_x, y + perp_y 
            x3, y3 = x1 + perp_x, y1 + perp_y
            x4, y4 = x - perp_x, y - perp_y
            x5, y5 = x1 - perp_x, y1 - perp_y

        xi, yi = line_intersection(
            x, y, *get_rotation_in_line(x, y, x2, y2, angle * factor), x3, y3, x2, y2
        ) # Ponto de interseção cor 0

        xin, yin = line_intersection(
            x, y, *get_rotation_in_line(x, y, x4, y4, -angle * factor), x5, y5, x4, y4
        ) # Ponto de interseção cor 1

        return x3, y3, x5, y5, xi, yi, xin, yin

    def draw_hexagon(self, x, y, size, rotation=0, colors=None, color=255):
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
            self.draw_map(vertices, color)

        return vertices
