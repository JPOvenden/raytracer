
from vectorMultiplier import Point, Vector

class World:
    def __init__(self, gravity):
        self.gravity = gravity

class Projectile:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

def tick(world, projectile):
    position = projectile.position + projectile.velocity
    velocity = projectile.velocity + world.gravity
    return Projectile(position, velocity)

start = Point(0, 1, 0)
velocity = Vector(1, 1.8, 0).normalize() * 11.25
projectile = Projectile(start, vel)
gravity = Vector(0, -0.1, 0)
world = World(gravity)
tick = 0

while p.position.y >= 0:
    print(f"Tick {tick}: Position {projectile.position}")
    projectile = tick(w, p)
    tick += 1
