from typing import List
import random
import pyxel # type: ignore
from .config import Config
from .utility_classes import Box, Vector, Event, EventObserver, Utils
from .game_events import EventUp, EventDown, EventLeft, EventRight


class GameContainer:
    def __init__(self):
        self.objects: List['GameObject'] = []
        self.score = 0
        self.collision_mapping = {}
    
    def add(self, obj: 'GameObject'):
        self.objects.append(obj)
    
    def remove(self, obj: 'GameObject'):
        self.objects.remove(obj)
    
    def get_object_around_vector(self, vector, margin=1):
        valid = []
        for obj in self.objects:
            if Utils.point_in_box(obj.box.center, Box(
                vector.x - margin,
                vector.y - margin,
                margin + margin,
                margin + margin
                )):
                valid.append(obj)
        
        return valid
    
    def __getitem__(self, item):
        return self.objects[item]
    
    def __setitem__(self, index, value):
        self.objects[index] = value


class GameObject:
    is_wall = False

    def __init__(self, game, x: int, y: int, width: int, height: int):
        self.pos = Vector(x, y)
        self.move_vector = Vector(0, 0)
        self.width = width
        self.height = height
        self.box = Box(self.pos.x, self.pos.y, self.width, self.height)
        self.game: GameContainer = game

    def update(self):
        self.box.move_to(self.pos)

    def draw(self):
        if Config.DEBUG:
            pyxel.rectb(
                x=self.box.u,
                y=self.box.v,
                w=self.box.w,
                h=self.box.h,
                col=pyxel.COLOR_RED
            )

            margin = Config.COLLISION_MARGIN
            pyxel.rectb(
                x=self.box.center.x - margin,
                y=self.box.center.y - margin,
                w=margin + margin,
                h=margin + margin,
                col=pyxel.COLOR_GREEN
            )

            pyxel.circ(
                self.box.center.x,
                self.box.center.y,
                2,
                pyxel.COLOR_GREEN
            )
    
    def reset(self):
        pass

    def collision(self, object_box: Box) -> bool:
        return (
            Utils.box_collision_check(self.box, object_box) or
            Utils.box_collision_check(object_box, self.box)
            )


class Monster(GameObject, EventObserver):
    def __init__(self, game, x, y):
        self.animation_state = 0
        self.animation_count = 0
        super().__init__(game,x, y, width=16, height=16)

    def update(self):
        self.move(self.move_vector.x, self.move_vector.y)
        self.move_vector = Vector(0, 0)
        super().update()

    def draw(self):
        if self.animation_state == 0:
            pyxel.blt(
                x=self.pos.x,
                y=self.pos.y,
                img=0, # image 0,1 or 2
                u=0,
                v=16,
                w=self.width,
                h=self.height,
                colkey=0
                )
        if self.animation_state == 1:
            pyxel.blt(
                x=self.pos.x,
                y=self.pos.y,
                img=0, # image 0,1 or 2
                u=0,
                v=32,
                w=self.width,
                h=self.height,
                colkey=0
                )
        super().draw()

    def move(self, x, y):
        def collision_check(x, y):
            box = self.box.copy()
            box.move_to(Vector(self.pos.x + x, self.pos.y + y))
            for obj in self.game.get_object_around_vector(self.box.center, Config.COLLISION_MARGIN):
                if obj.is_wall and obj.collision(box):
                    return False
            return True
        
        collision = collision_check(x, y)
        while (x != 0 or y != 0) and not collision:
            if x < 0:
                x += 1
            if x > 0:
                x -= 1
            if y < 0:
                y += 1
            if y > 0:
                y -= 1
            collision = collision_check(x, y)
        
        if (x != 0 or y != 0) and collision:
            self.pos.move(x,y)
            self._change_animation_state()

    def react(self, event: Event):
        speed = 4

        if isinstance(event, EventUp):
            self.move_vector.move(0, -1 * speed)
        if isinstance(event, EventDown):
            self.move_vector.move(0, speed)
        if isinstance(event, EventLeft):
            self.move_vector.move(-1 * speed, 0)
        if isinstance(event, EventRight):
            self.move_vector.move(speed, 0)
    
    def _change_animation_state(self):
        self.animation_count += 1
        if self.animation_count > 5:
            if self.animation_state == 0:
                self.animation_state = 1
            else:
                self.animation_state = 0
            self.animation_count = 0


class Enemy(GameObject, EventObserver):
    def __init__(self, game, x, y):
        self.move_counter = 0
        self.move_vector = Vector(0, 0)
        # self.collided_with = set()
        super().__init__(game,x, y, 5, 8)

    def update(self):
        if self.move_counter >= 10:
            # self.move_vector = Vector(random.randint(-2,2), random.randint(-2,2))
            self.move_counter = 0
        
        self.move(self.move_vector.x, self.move_vector.y)
        self.move_counter += 1

        self.move_vector = Vector(0, 0)
        super().update()

    def draw(self):
        pyxel.blt(
            x=self.pos.x,
            y=self.pos.y,
            img=0, # image 0,1 or 2
            u=9,
            v=0,
            w=self.width,
            h=self.height,
            colkey=0
            )
        super().draw()

    def move(self, x, y):
        box = self.box.copy()
        box.move_to(self.pos.copy().move(x, y))
        print(box)
        can_move = True
        for obj in self.game.get_object_around_vector(box.center, Config.COLLISION_MARGIN):
            if isinstance(obj, Monster) and obj.collision(box):
                self.game.score -= 1
                self.game.objects.remove(self)
            if obj.is_wall and obj.collision(box):
                can_move = False
        
        if can_move:
            self.pos.move(x,y)

    def react(self, event: Event):
        speed = 4

        if isinstance(event, EventUp):
            self.move_vector.move(0, -1 * speed)
        if isinstance(event, EventDown):
            self.move_vector.move(0, speed)
        if isinstance(event, EventLeft):
            self.move_vector.move(-1 * speed, 0)
        if isinstance(event, EventRight):
            self.move_vector.move(speed, 0)


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
        super().draw()
