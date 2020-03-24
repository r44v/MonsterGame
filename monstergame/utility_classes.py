class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Vector(x: {self.x}, y: {self.y})"


class Box:
    def __init__(self, u, v, w, h):
        self.u = u
        self.v = v
        self.w = w
        self.h = h

        self.left_top_vector = Vector(self.u, self.v)
        self.right_top_vector = Vector(self.u + self.w, v)
        self.right_bottom_vector = Vector(self.u + self.w, self.v + self.h)
        self.left_bottom_vector = Vector(self.u, self.v + self.h)
    
    def move(self, vector: Vector):
        self.u = vector.x
        self.v = vector.y

        self.left_top_vector = Vector(self.u, self.v)
        self.right_top_vector = Vector(self.u + self.w, self.v)
        self.right_bottom_vector = Vector(self.u + self.w, self.v + self.h)
        self.left_bottom_vector = Vector(self.u, self.v + self.h)
    
    def __repr__(self):
        return f"Box(u: {self.u}, v: {self.v}, w: {self.w}, h: {self.h})"


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
