from vectorMultiplier import Color

class Canvas:
    def __init__(self, width, height, color=None):
        self.width = width
        self.height = height
        self.color = Color(0, 0, 0) if not color else color
        self.grid = [[self.color] * self.width for _ in range(self.height)]

    def write_pixel(self, x, y, color):
        self.grid[y][x] = color

    def pixel(self, x, y):
        return self.grid[y][x]

    def header(self):
        return f'P3\n{self.width} {self.height}\n255\n'
    
    def to_file(self, filename):
        with open(filename, 'w') as ppm_file:
            ppm_file.write(self.header())
            for row in self.grid:
                for elem in row:
                    ppm_file.write(f'{elem.x} {elem.y} {elem.z}\n')

v = Canvas(800, 600)
g = 100      
for s in range(g, 700):
    for b in range(g, 500):
        v.write_pixel(s, b, Color(255, 255, 255))

v.to_file('canvas.ppm')

