import random
import time
import math
from vector import VECTOR_I, Vector


def generate_polygon(vertex_count: int, min: Vector, max: Vector):
    def sortAngle(v: Vector):
        norm_v = v.normalize()
        dot_v = norm_v.dot(VECTOR_I)
        cross_v = VECTOR_I.cross(norm_v)
        sign = math.copysign(1, cross_v)

        return math.acos(dot_v) * sign

    random.seed(time.time())

    size = max.sub(min)
    size.x /= 2
    size.y /= 2

    polygon = []
    for i in range(vertex_count):
        x = random.random() * size.x  # + (min.x + size.x)
        y = random.random() * size.y  # + (min.y + size.y)
        direction = -1.0 if random.random() >= 0.5 else 1.0
        polygon.append(Vector(x * direction, y * direction))

    polygon.sort(key=sortAngle)

    # remove all the collinear vectors
    ok = False
    while True:
        found = False
        for i in range(len(polygon)):
            i1 = (i - 1) % len(polygon)
            i2 = (i + 1) % len(polygon)

            a = polygon[i]
            b = polygon[i1]
            c = polygon[i2]

            ab = b.sub(a)
            ac = c.sub(a)

            if ab.cross(ac) == 0:
                bc = c.sub(b)

                ab_len = ab.length_sq()
                ac_len = ac.length_sq()
                bc_len = bc.length_sq()

                if ab_len > ac_len and ab_len > bc_len:
                    polygon.remove(c)
                elif ac_len > ab_len and ac_len > bc_len:
                    polygon.remove(b)
                elif bc_len > ab_len and bc_len > ac_len:
                    polygon.remove(a)
                found = True
                break

        if not found:
            break

    for i in range(len(polygon)):
        polygon[i].x += (min.x + size.x)
        polygon[i].y += (min.y + size.y)

    return polygon
