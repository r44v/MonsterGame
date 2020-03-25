from typing import List
import random
import pyxel
from .utility_classes import Position, Box, Vector, Event, EventObserver
from .config import DEBUG
from .game_events import EventUp, EventDown, EventLeft, EventRight


class GameContainer:
    def __init__(self):
        self.objects: List['GameObject'] = []
        self.score = 0
    
    def add(self, obj: 'GameObject'):
        self.objects.append(obj)
    
    def remove(self, obj: 'GameObject'):
        self.objects.remove(obj)
    
    def __getitem__(self, item):
        return self.objects[item]
    
    def __setitem__(self, index, value):
        self.objects[index] = value


class GameObject:
    is_wall = False

    def __init__(self, game, x: int, y: int, width: int, height: int):
        self.pos = Position(x, y)
        self.box = Box(self.pos.x, self.pos.y, width, height)
        self.game: GameContainer = game

    def update(self):
        self.box.move(self.pos)

    def draw(self):
        if DEBUG:
            pyxel.rectb(
                x=self.box.u,
                y=self.box.v,
                w=self.box.w,
                h=self.box.h,
                col=pyxel.COLOR_RED
            )

    def collision(self, object_box: Box) -> bool:
        return (
            self._box_collision_check(self.box, object_box) or
            self._box_collision_check(object_box, self.box))
    
    def _box_collision_check(self, outer_box: Box, inner_box: Box) -> bool:
        return (
            self._point_in_box(outer_box.left_top_vector    , inner_box) or
            self._point_in_box(outer_box.right_top_vector   , inner_box) or
            self._point_in_box(outer_box.right_bottom_vector, inner_box) or
            self._point_in_box(outer_box.left_bottom_vector , inner_box)
            )

    def _point_in_box(self, point: Vector, box: Box) -> bool:
        return (box.u <= point.x <= (box.u + box.w)
            and box.v <= point.y <= (box.v + box.h))


class Monster(GameObject, EventObserver):
    _WIDTH = 16
    _HEIGHT = 16

    def __init__(self, game, x, y):
        self.animation_state = 0
        self.animation_count = 0
        super().__init__(game,x, y, self._WIDTH, self._HEIGHT)

    def update(self):        
        super().update()

    def draw(self):
        if self.animation_state == 0:
            pyxel.blt(
                x=self.pos.x,
                y=self.pos.y,
                img=0, # image 0,1 or 2
                u=0,
                v=16,
                w=self._WIDTH,
                h=self._HEIGHT,
                colkey=0
                )
        if self.animation_state == 1:
            pyxel.blt(
                x=self.pos.x,
                y=self.pos.y,
                img=0, # image 0,1 or 2
                u=0,
                v=32,
                w=self._WIDTH,
                h=self._HEIGHT,
                colkey=0
                )
        super().draw()

    def move(self, x, y):
        for obj in self.game.objects:
            box = self.box.copy()
            box.move(Vector(self.pos.x + x, self.pos.y + y))
            if obj.is_wall and obj.collision(box):
                return
        self.pos.x += x
        self.pos.y += y
        self._change_animation_state()

    def react(self, event: Event):
        speed = 4
        if isinstance(event, EventUp):
            self.move(0, -1 * speed)
        if isinstance(event, EventDown):
            self.move(0, speed)
        if isinstance(event, EventLeft):
            self.move(-1 * speed, 0)
        if isinstance(event, EventRight):
            self.move(speed, 0)

    def _change_animation_state(self):
        self.animation_count += 1
        if self.animation_count > 5:
            if self.animation_state == 0:
                self.animation_state = 1
            else:
                self.animation_state = 0
            self.animation_count = 0


class Enemy(GameObject, EventObserver):
    _WIDTH = 5
    _HEIGHT = 8
    is_wall = True

    def __init__(self, game, x, y):
        self.move_counter = 0
        self.move_vector = Vector(0, 0)
        super().__init__(game,x, y, self._WIDTH, self._HEIGHT)

    def update(self):
        if self.move_counter >= 10:
            self.move_vector = Vector(random.randint(-2,2), random.randint(-2,2))
            self.move_counter = 0
        
        self.move(self.move_vector.x, self.move_vector.y)
        self.move_counter += 1
        
        for obj in self.game.objects:
            if isinstance(obj, Monster) and obj.collision(self.box):
                self.game.score -= 1


        super().update()

    def draw(self):
        pyxel.blt(
            x=self.pos.x,
            y=self.pos.y,
            img=0, # image 0,1 or 2
            u=9,
            v=0,
            w=self._WIDTH,
            h=self._HEIGHT,
            colkey=0
            )
        super().draw()

    def move(self, x, y):
        for obj in self.game.objects:
            if obj is self:
                continue
            box = self.box.copy()
            box.move(Vector(self.pos.x + x, self.pos.y + y))
            if obj.is_wall and obj.collision(box):
                return
        self.pos.x += x
        self.pos.y += y

    def react(self, event: Event):
        pass

class Corpse(GameObject):
    _WIDTH = 16
    _HEIGHT = 3

    def __init__(self, game, x, y):
        super().__init__(game, x, y, self._WIDTH, self._HEIGHT)

    def update(self):
        super().update()

    def draw(self):
        pyxel.blt(
            x=self.pos.x,
            y=self.pos.y,
            img=0,
            u=0,
            v=53,
            w=16,
            h=3,
            colkey=0
            )
        super().draw()


class Boundary(GameObject):
    is_wall = True

    def __init__(self, game, x, y, width, height):
        super().__init__(game, x, y, width, height)

    def update(self):
        super().update()

    def draw(self):
        pyxel.blt(
            x=self.pos.x,
            y=self.pos.y,
            img=0,
            u=0,
            v=0,
            w=8,
            h=8,
            colkey=0
            )
