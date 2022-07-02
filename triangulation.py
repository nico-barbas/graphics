import arcade
from vector import Vector


class Open_Set:
    def __init__(self, count) -> None:
        self.count = count
        self.indices = [i for i in range(count)]

    def remove(self, r_index):
        at = -1
        for i in range(self.count):
            index = self.indices[i]
            if index == r_index:
                at = i
                break

        if at != -1:
            for i in range(at, self.count-1):
                self.indices[i] = self.indices[i+1]
            self.count -= 1

    def next_index(self, at: int) -> int:
        return self.indices[(at+1) % self.count]

    def previous_index(self, at: int) -> int:
        return self.indices[(at-1) % self.count]


polygon = [Vector(1, 1),
           Vector(2, 0),
           Vector(2.5, 0.5),
           Vector(2, 1),
           Vector(2.5, 1.5),
           Vector(2, 2),
           ]

open_set = Open_Set(len(polygon))

triangles = {
    "tri_count": 0,
    "tri": [],
}

CLOCKWISE = 0
COUNTER_CLOCKWISE = 1
ORDER = COUNTER_CLOCKWISE


def order_polygon():
    bottom_most = Vector(10, -10)
    ti0 = -1
    for p, i in polygon:
        if p.y < bottom_most.y:
            bottom_most = p
            ti0 = i
        elif p.y == bottom_most.y:
            if p.x > bottom_most.x:
                bottom_most = p
                ti0 = i

    if ti0 != -1:
        ti1 = (ti0 - 1) % len(polygon)
        ti2 = (ti0 + 1) % len(polygon)

        ta = polygon[ti1].sub(bottom_most)
        tb = polygon[ti2].sub(bottom_most)

        cross_tab = ta.cross(tb)
        if not cross_tab < 0:
            polygon.reverse()


def triangulate():
    def check_edge(a: Vector, b: Vector) -> bool:
        cross_ab = a.cross(b)
        return cross_ab > 0

    def point_in_triangle(t_info, p: Vector) -> bool:
        a_to_point = p.sub(t_info["a"])
        if check_edge(t_info["ab"], a_to_point):
            return False
        if check_edge(a_to_point, t_info["ac"]):
            return False

        c_to_point = p.sub(t_info["c"])
        if check_edge(t_info["ca"], c_to_point):
            return False
        if check_edge(c_to_point, t_info["cb"]):
            return False

        return True

    def add_triangle(i0, i1, i2):
        triangles["tri_count"] += 1
        triangles["tri"].append([i0, i1, i2])

    while open_set.count > 3:
        for i in range(open_set.count):
            i0 = open_set.indices[i]
            i1 = open_set.previous_index(i)
            i2 = open_set.next_index(i)

            a = polygon[i0]
            b = polygon[i1]
            c = polygon[i2]

            ab = b.sub(a)
            ac = c.sub(a)

            cross_ab = ab.cross(ac)
            if cross_ab < 0:
                is_ear = True
                tri_info = {
                    "a": a,
                    "b": b,
                    "c": c,
                    "ab": ab,
                    "ac": ac,
                    "ca": a.sub(c),
                    "cb": b.sub(c),
                }
                for j in range(open_set.count):
                    check = open_set.indices[j]
                    if check == i0 or check == i1 or check == i2:
                        continue

                    inside_triangle = point_in_triangle(
                        tri_info, polygon[check])
                    if inside_triangle:
                        is_ear = False
                        break

                if is_ear:
                    open_set.remove(i0)
                    add_triangle(i0, i2, i1)
                    break

    add_triangle(
        open_set.indices[0],
        open_set.indices[2],
        open_set.indices[1],
    )
    open_set.count = 0


triangulate()
print(triangles["tri_count"])
for tri in triangles["tri"]:
    print(tri)


class Display(arcade.Window):
    def __init__(self, w: int, h: int, t: str):
        super().__init__(w, h, t)
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.start_render()
        for tri in triangles["tri"]:
            a = polygon[tri[0]]
            b = polygon[tri[1]]
            c = polygon[tri[2]]

            ax = a.x * 100
            ay = a.y * 100
            bx = b.x * 100
            by = b.y * 100
            cx = c.x * 100
            cy = c.y * 100
            arcade.draw_line(ax, ay, bx, by, arcade.color.WHITE, 1)
            arcade.draw_line(ax, ay, cx, cy, arcade.color.WHITE, 1)
            arcade.draw_line(bx, by, cx, cy, arcade.color.WHITE, 1)


display = Display(800, 600, "Triangulation")
arcade.run()
