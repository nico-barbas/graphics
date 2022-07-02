import math


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def sub(self, v):
        return Vector(self.x - v.x, self.y - v.y)

    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def cross(self, v):
        return self.x*v.y - v.x*self.y

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length_sq(self) -> float:
        return self.x * self.x + self.y * self.y

    def normalize(self):
        l = self.length()
        return Vector(self.x / l, self.y / l)


VECTOR_I = Vector(0, 1)
VECTOR_J = Vector(1, 0)
