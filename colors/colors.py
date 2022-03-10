from collections import defaultdict
from os import makedirs
from PIL import Image
import random

#   NAME, PANTONE, hex RGB
COLORS = [
    ("White", "-", "ffffff"),
    ("Turquoise", "3255U", "00cfbb"),
    ("Pastel Green", "0921U", "78e6d0"),
    ("Pastel Yellow", "0131U", "fbf59b"),
    ("Pastel Magenta", "0521U", "f8aadd"),
    ("Violet", "0631U", "ba93df"),
    ("Pastel Blue", "0821U", "6cd1ef"),
]

SCALE = 32
GRID_SIZE = (15, 6)

# https://stackoverflow.com/questions/2576296/using-python-tuples-as-vectors
class Vector(tuple):
    def __add__(self, a):
        # TODO: check lengths are compatable.
        return Vector(x + y for x, y in zip(self, a))

    def __mul__(self, c):
        return Vector(x * c for x in self)

    def __rmul__(self, c):
        return Vector(c * x for x in self)


# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def reset_base_matrix():
    PINK = 4
    WHITE = 0

    base_matrix = defaultdict(lambda: None)
    base_matrix[Vector((14, 1))] = PINK
    base_matrix[Vector((4, 3))] = WHITE
    base_matrix[Vector((8, 3))] = WHITE
    base_matrix[Vector((4, 5))] = WHITE
    base_matrix[Vector((8, 5))] = WHITE
    return base_matrix

def generate_matrix(matrix):
    colors = [hex_to_rgb(color[2]) for color in COLORS]
    count = len(colors)
    # random_color_i = random.randint(0, count - 1)
    # random_color_rgb = colors[random_color_i]

    # return [colors[random.randint(0, count - 1)] for _ in range(0, GRID_SIZE[0] * GRID_SIZE[1])]
    # matrix = [[-1] * GRID_SIZE[1]] * GRID_SIZE[0]
    for y in range(GRID_SIZE[1]):
        for x in range(GRID_SIZE[0]):
            if matrix[Vector((x, y))] is not None:
                continue
            while True:
                random_color = random.randint(0, count - 1)
                for offset in [Vector((-1, 0)), Vector((0, -1)), Vector((1, 0)), Vector((0, 1))]:
                    if matrix[Vector((x, y)) + offset] == random_color:
                        break
                else:
                    matrix[Vector((x, y))] = random_color
                    break

    return [
        colors[matrix[Vector((x, y))]]
        for y in range(GRID_SIZE[1])
        for _ in range(SCALE)
        for x in range(GRID_SIZE[0])
        for _ in range(SCALE)
    ]


makedirs('./output', exist_ok=True)

for i in range(50):
    matrix = generate_matrix(reset_base_matrix())

    im = Image.new('RGB', tuple(i * SCALE for i in GRID_SIZE))
    im.putdata(matrix)
    im.save('./output/outpu-%s.png' % i)
