from typing import List
import random

import pyxel

from .config import Config
from .utility_classes import Box, Vector, Event, EventObserver, Utils
from .game_events import EventUp, EventDown, EventLeft, EventRight


class GameContainer:
    def __init__(self):
        self.objects: List['GameObject'] = []
        self.unloaded: List['GameObject'] = []
        self.near_objects: List['GameObject'] = []
        self.player: 'GameObject' = None
        self.background_x = 0
        self.playable_area = Box(0, 0 , Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        self.score = 0
    
    def set_player(self, player: 'GameObject'):
        self.player = player
    
    def add(self, obj: 'GameObject'):
        self.objects.append(obj)
    
    def remove(self, obj: 'GameObject'):
        self.objects.remove(obj)
    
    def in_game_area(self, box: Box):
        if (box.u < self.playable_area.u
            or box.v < self.playable_area.v
            or box.u + box.w > self.playable_area.u + self.playable_area.w
            or box.v + box.h > self.playable_area.v + self.playable_area.h):
            
            return False
        return True
    
    def __getitem__(self, item):
        return self.objects[item]
    
    def __setitem__(self, index, value):
        self.objects[index] = value


class GameObject:
    is_wall = False
    width = 0
    height = 0
    
    def __init__(self, game: GameContainer, x: int, y: int, width: int, height: int, parent: Vector = Vector(0,0)):
        self.game: GameContainer = game
        self.parent = parent
        self.width = width
        self.height = height
        self.collided = False
        self.box = Box(x, y, self.width, self.height)
        self.move_vector = Vector(0, 0)

    def update(self):
        pass

    def draw(self):
        pass
    
    def reset(self):
        pass

    def collision(self, object_box: Box) -> bool:
        self_box = self.box.copy().move(self.parent)
        if Utils.box_collision_check_efficient(self_box, object_box):
            self.collided = True
            return True
        return False
    
    def move(self, x, y):
        can_move = True
        new_box = self.box.copy().move(Vector(x, y))
        for obj in self.game.objects:
            if (obj is not self
                and obj.collision(new_box)
                and obj.is_wall
                ):
                can_move = False
        
        if (x != 0 or y != 0) and (not can_move or not self.game.in_game_area(new_box)):
            if x < 0:
                x += 1
            if x > 0:
                x -= 1
            if y < 0:
                y += 1
            if y > 0:
                y -= 1
            return self.move(x, y)

        self.box.move(Vector(self.parent.x + x, self.parent.y + y))
        return True


class Player(GameObject, EventObserver):
    height = 16
    width = 16
    is_wall = True

    def __init__(self, game, x, y, parent: Vector = Vector(0,0)):
        self.animation_count = 2  # total animation frames
        self.animation_frame = 0  # current animation
        self.animation_steps = 5  # frames per animation

        super().__init__(game, x, y, width=self.width, height=self.height, parent=parent)

    def update(self):
        if self.move_vector != Vector(0, 0):
            if self.move(self.move_vector.x, self.move_vector.y):
                self._change_animation_state()
        self.move_vector = Vector(0, 0)
        super().update()

    def draw(self):
        if self.animation_frame == 0:
            pyxel.blt(
                x=self.box.u,
                y=self.box.v,
                img=0, # image 0,1 or 2
                u=0,
                v=16,
                w=self.width,
                h=self.height,
                colkey=0
                )
        if self.animation_frame == 1:
            pyxel.blt(
                x=self.box.u,
                y=self.box.v,
                img=0, # image 0,1 or 2
                u=0,
                v=32,
                w=self.width,
                h=self.height,
                colkey=0
                )
        if Config.DEBUG:
            box = self.box.copy().grow(Config.COLLISION_MARGIN)
            pyxel.rectb(
                box.u,
                box.v,
                box.w,
                box.h,
                5
            )
        super().draw()

    def react(self, event: Event):
        speed = 4
        if isinstance(event, EventUp):
            self.move_vector.move(0, -1 * speed)
            self._change_animation_state()
        if isinstance(event, EventDown):
            self.move_vector.move(0, speed)
            self._change_animation_state()
        if isinstance(event, EventLeft):
            self.move_vector.move(-1 * speed, 0)
            self._change_animation_state()
        if isinstance(event, EventRight):
            self.move_vector.move(speed, 0)
            self._change_animation_state()
        

    def _change_animation_state(self):
        if pyxel.frame_count % self.animation_steps == 0:
            self.animation_frame += 1
        if self.animation_frame >= self.animation_count:
            self.animation_frame = 0
        
     
class Background(GameObject, EventObserver):
    def __init__(self, game, x, y):
        self.animation_count = 1  # total animation frames
        self.animation_frame = 0  # current animation
        self.animation_steps = 10  # frames per animation        
        self.objects = []

        for i in range(10):
            self.objects.append(Boundary(
                game, 
                random.randint(x, x + game.playable_area.w),
                random.randint(y, y + game.playable_area.h), 8, 8     
            ))

        super().__init__(
            game,
            x,
            y,
            width=game.playable_area.w,
            height=game.playable_area.h)

    def update(self):
        self.move_all()
        self.move_vector = Vector(0, 0)
        for obj in self.objects:
            obj.update()
        super().update()
    
    def move_all(self):
        if self.move_vector == Vector(0, 0):
            return
        can_move = True
        for obj in self.objects:
            can_move = self.move_obj(obj)
            if not can_move:
                break

        if can_move:
            for obj in self.objects:
                obj.box.move(Vector(self.move_vector.x, self.move_vector.y))
            self.box.move(Vector(self.move_vector.x, self.move_vector.y))
        else:
            if self.move_vector.x < 0:
                self.move_vector.x += 1
            if self.move_vector.x > 0:
                self.move_vector.x -= 1
            if self.move_vector.y < 0:
               self.move_vector.y += 1
            if self.move_vector.y > 0:
                self.move_vector.y -= 1
            self.move_all()
        
    def move_obj(self, obj: GameObject):
        new_box = obj.box.copy()
        new_box.move_to(Vector(
            obj.box.u + self.move_vector.x,
            obj.box.v + self.move_vector.y
        ))
        for game_obj in self.game.objects:
            if (game_obj is not self and game_obj.collision(new_box)):
                return False
        return True
        
    def draw(self):
        for obj in self.objects:
            if obj.collision(Box(0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)):
                obj.draw()

    def react(self, event: Event):
        speed = 4

        if isinstance(event, EventLeft):
            self.move_vector.move(-1 * speed, 0)
        if isinstance(event, EventRight):
            self.move_vector.move(speed, 0)

    def collision(self, object_box: Box) -> bool:
        for obj in self.objects:
            collided = Utils.box_collision_check_efficient(obj.box, object_box)
            if collided:
                return True
        return False


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
                x=self.box.u,
                y=self.box.v,
                img=0, # image 0,1 or 2
                u=0,
                v=16,
                w=self.width,
                h=self.height,
                colkey=0
                )
        if self.animation_state == 1:
            pyxel.blt(
                x=self.box.u,
                y=self.box.v,
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
            box.move_to(Vector(self.box.u + x, self.box.v + y))
            for obj in self.game.objects:
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
            self.box.move(Vector(x,y))
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
        super().__init__(game,x, y, 5, 8)

    def update(self):
        if self.move_counter >= 10:
            self.move_vector = Vector(random.randint(-2,2), random.randint(-2,2))
            self.move_counter = 0
        self.move_counter += 1
        self.move(self.move_vector.x, self.move_vector.y)
        super().update()

    def draw(self):
        pyxel.blt(
            x=self.box.u,
            y=self.box.v,
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
        p = self.box.left_top_vector.copy().move(x, y)
        box.move_to(p)
        can_move = True
        for obj in self.game.objects:
            if isinstance(obj, Monster) or obj.is_wall:
                collision = Utils.box_collision_check_efficient(obj.box, box)
                if isinstance(obj, Monster) and collision:
                    self.game.score -= 1
                    self.game.objects.remove(self)
                if obj.is_wall and collision:
                    can_move = False
        
        if can_move:
            self.box.move(Vector(x,y))

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
            x=self.box.u,
            y=self.box.v,
            img=0,
            u=0,
            v=53,
            w=16,
            h=3,
            colkey=0
            )
        super().draw()


class TextBox(GameObject):
    is_wall = True

    def __init__(self, game, x, y, width, parent: Vector = Vector(0,0), color: int=7, line1 = "", line2 = ""):
        self.line1 = line1
        self.line2 = line2
        self.color = color
        super().__init__(game, x, y, width, 19, parent = parent)

    def update(self):
        super().update()

    def draw(self):
        pyxel.rectb(
            x= self.parent.x + self.box.u,
            y= self.parent.y + self.box.v,
            w= self.width,
            h= self.height,
            col=self.color
            )
        
        pyxel.text(
            x= self.parent.x + self.box.u + 3,
            y= self.parent.y + self.box.v + 3,
            s=self.line1,
            col=self.color
        )

        pyxel.text(
            x= self.parent.x + self.box.u + 3,
            y= self.parent.y + self.box.v + 11,
            s=self.line2,
            col=self.color
        )
        super().draw()


class Boundary(GameObject):
    is_wall = True

    def __init__(self, game, x, y, width, height, parent: Vector = Vector(0,0)):
        super().__init__(game, x, y, width, height, parent = parent)

    def update(self):
        super().update()

    def draw(self):
        pyxel.blt(
            x= self.parent.x + self.box.u,
            y= self.parent.y + self.box.v,
            img= 0,
            u= 0,
            v= 0,
            w= 8,
            h= 8,
            colkey= 0
            )
        super().draw()


class Item(GameObject, Event):
    is_wall = False

    def __init__(self, game, x, y, tile_x: int, tile_y: int, parent: Vector = Vector(0,0)):
        self.tile_x = tile_x
        self.tile_y = tile_y
        Event.__init__(self)
        super().__init__(game, x, y, 8, 8, parent = parent)

    def draw(self):
        pyxel.blt(
            x= self.parent.x + self.box.u,
            y= self.parent.y + self.box.v,
            img= 0,
            u= self.tile_x,
            v= self.tile_y,
            w= self.width,
            h= self.height,
            colkey= 0
            )
        super().draw()

    def update(self):
        if self.collided:
            self.trigger()
        super().update()    
    
    def trigger(self):
        self.notify()


class Level(EventObserver):
    def __init__(self, game: GameContainer, x: int, y: int, width: int, height: int):
        self.game = game
        self.box = Box(x, y, width, height)
        self.objects: List[GameObject] = []
        self.level_movement = Vector(0, 0)
        self.loaded = False
        self.setup()
    
    def update(self):
        if not Utils.box_collision_check_efficient(
            self.box,
            self.game.playable_area
        ):
            self.unload()
            return
        
        self.load()

    def draw(self):
        if not self.loaded:
            return
        
        pyxel.rect(
            self.box.u,
            self.box.v,
            self.box.w,
            self.box.h,
            1
        )
    
    def setup(self, *game_objects: List[GameObject]):
        for obj in game_objects:
            self.objects.append(obj)

    def react(self, event: Event):
        pass
     
    def move(self, x):
        self.box.move(Vector(x, 0))
    
    def load(self):
        if self.loaded:
            return 

        if Config.DEBUG:
            print(self, 'loaded')
        
        for obj in self.objects:
            self.game.objects.append(obj)
        self.loaded = True

    def unload(self):
        if not self.loaded:
            return
        
        if Config.DEBUG:
            print(self, 'unloaded')
        
        for obj in self.objects:
            self.game.objects.remove(obj)
        self.loaded = False
