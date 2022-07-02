import random
import time
from vector import Vector


def generate_polygon(vertex_count: int, min: Vector, max: Vector):
    def sortAngle(v):
        return

    random.seed(time.time())

    size = max.sub(min)
    size.x /= 2
    size.y /= 2

    polygon = []
    for i in range(vertex_count):
        x = random.random() * size.x #+ (min.x + size.x)
        y = random.random() * size.y #+ (min.y + size.y)
        direction = -1.0 if random.random() >= 0.5 else 1.0
        polygon.append(Vector(x * direction, y * direction))

    # polygon.sort(key=)
