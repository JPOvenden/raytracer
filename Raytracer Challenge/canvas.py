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
x = 800
y = 600
canvas = Canvas(x, y)
bleed = 100      
for pixelX in range(bleed, x - bleed):
    for pixel Y in range(bleed, y - bleed):
        canvas.write_pixel(s, b, Color(255, 255, 255))

canvas.to_file('canvas.ppm')

