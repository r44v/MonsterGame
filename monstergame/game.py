import pyxel
import math
import random

from .utility_classes import Position, Box, Vector

# Max screen size 256*256
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
DEBUG = True


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load("assets.pyxres")

        self.game_objects = [
            Monster(100, 100),
            Corpse(random.randint(10,246), random.randint(10,246)),
            Corpse(248,1)
        ]

        self.score = 0

        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        monster = self.game_objects[0]
        for corpse in self.game_objects[1:]:
            if monster.collision(corpse.box):
                self.game_objects[1] = Corpse(random.randint(10,246), random.randint(10,246))
                self.score += 1
         
        for obj in self.game_objects:
            obj.update()

    def draw(self):
        pyxel.cls(0)
        
        for obj in self.game_objects:
            obj.draw()

        pyxel.text(
            5,              # x-position of the text
            5,              # y position of the text
            str(f"Score {self.score}"), # displayed text as string
            7               # text color
            )
        
    def _point_in_box(self, point: Vector, box: Box) -> bool:
        if box.u <= point.x <= (box.u + box.w) and box.v <= point.y <= (box.v + box.h):
            return True
        else:
            return False


class GameObject:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.pos = Position(x, y)
        self.box = Box(self.pos.x, self.pos.y, width, height)
    
    def update(self):
        pass

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
        return (self._point_in_box(self.box.left_top_vector, object_box) 
            or self._point_in_box(self.box.right_top_vector, object_box)
            or self._point_in_box(self.box.right_bottom_vector, object_box)
            or self._point_in_box(self.box.left_bottom_vector, object_box))

    def _point_in_box(self, point: Vector, box: Box) -> bool:
        return (box.u <= point.x <= (box.u + box.w)
            and box.v <= point.y <= (box.v + box.h))


class Monster(GameObject):
    _WIDTH = 16
    _HEIGHT = 16

    def __init__(self, x, y):
        self.animation_state = 0
        self.animation_count = 0
        super().__init__(x, y, self._WIDTH, self._HEIGHT)

    def update(self):
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.pos.y -= 2
            self._change_animation_state()
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.pos.x += 2
            self._change_animation_state()
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.pos.y += 2
            self._change_animation_state()
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.pos.x -= 2
            self._change_animation_state()
        
        self.box.move(self.pos)

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
    
    def _change_animation_state(self):
        self.animation_count += 1
        if self.animation_count > 5:
            if self.animation_state == 0:
                self.animation_state = 1
            else:
                self.animation_state = 0
            self.animation_count = 0


class Corpse(GameObject):
    _WIDTH = 16
    _HEIGHT = 3

    def __init__(self, x, y):
        super().__init__(x, y, self._WIDTH, self._HEIGHT)

    def update(self):
        super.update()

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
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

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

App()