class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def sub(self, v):
        return Vector(self.x - v.x, self.y - v.y)

    def cross(self, v):
        return self.x*v.y - v.x*self.y