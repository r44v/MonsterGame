from abc import ABC, abstractmethod

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, x, y):
        if x == 0 and y == 0:
            return self
        print(self)
        self.x += x
        self.y += y
        return self
    
    def copy(self):
        return Vector(self.x, self.y)

    def __repr__(self):
        return f"Vector(x: {self.x}, y: {self.y})"


class Box:
    def __init__(self, u: int, v: int, w: int, h: int):
        self.u = u
        self.v = v
        self.w = w
        self.h = h

        self.left_top_vector = Vector(self.u, self.v)
        self.right_top_vector = Vector(self.u + self.w, v)
        self.right_bottom_vector = Vector(self.u + self.w, self.v + self.h)
        self.left_bottom_vector = Vector(self.u, self.v + self.h)
        self.center = Vector((self.u + self.u + self.w) / 2, (self.v + self.v + self.h) / 2)
    
    def move_to(self, vector: Vector):
        self.u = vector.x
        self.v = vector.y

        self.left_top_vector = Vector(self.u, self.v)
        self.right_top_vector = Vector(self.u + self.w, self.v)
        self.right_bottom_vector = Vector(self.u + self.w, self.v + self.h)
        self.left_bottom_vector = Vector(self.u, self.v + self.h)
        self.center = Vector((self.u + self.u + self.w) / 2, (self.v + self.v + self.h) / 2)
        return self
    
    def copy(self):
        return Box(self.u, self.v, self.w, self.h)
    
    def __repr__(self):
        return f"Box(u: {self.u}, v: {self.v}, w: {self.w}, h: {self.h})"


class Event:
    def __init__(self):
        self._subscribers = []
    
    def subscribe(self, observer: "EventObserver"):
        self._subscribers.append(observer)
    
    def unsubscribe(self, observer: "EventObserver"):
        self._subscribers.remove(observer)

    def notify(self):
        for subscriber in self._subscribers:
            subscriber.react(self)
    
    @abstractmethod
    def trigger(self):
        pass


class EventObserver(ABC):
    @abstractmethod
    def react(self, event: Event):
        pass


class Utils:
    @staticmethod
    def box_collision_check(outer_box: Box, inner_box: Box) -> bool:
        return (
            Utils.point_in_box(outer_box.left_top_vector    , inner_box) or
            Utils.point_in_box(outer_box.right_top_vector   , inner_box) or
            Utils.point_in_box(outer_box.right_bottom_vector, inner_box) or
            Utils.point_in_box(outer_box.left_bottom_vector , inner_box)
            )

    @staticmethod
    def point_in_box(point: Vector, box: Box) -> bool:
        return (box.u < point.x < (box.u + box.w)
            and box.v < point.y < (box.v + box.h))
