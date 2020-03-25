import pyxel # type: ignore
import math
import random
from enum import Enum
from .config import Config
from .game_classes import GameContainer, GameObject, Boundary, Corpse, Monster, Enemy
from .game_events import EventUp, EventDown, EventLeft, EventRight
from .utility_classes import Box, Vector, Event


"""
TODO

- [ ] GameContainer has collisions list for each object
- [ ] User collission detected only for used movement
"""

class GameState(Enum):
    PLAYING = 1,
    GAME_OVER = 2
    WON = 3

class App:
    def __init__(self):
        pyxel.init(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        pyxel.load("assets.pyxres")

        self.new_game()

        pyxel.run(self.update, self.draw)
    
    def new_game(self):
        self.game_objects = GameContainer()
        monster = Monster(self.game_objects, 100, 100)
        self.game_objects.add(monster)
        self.game_objects.add(Corpse(self.game_objects, random.randint(16,240), random.randint(32,240)))
        self.game_objects.add(Enemy(self.game_objects, random.randint(16,256-16), 256-32))
        for i in range(0,256, 8):
            self.game_objects.add(Boundary(self.game_objects, i, 16, 8, 8))
            self.game_objects.add(Boundary(self.game_objects, i, 256-8, 8, 8))
        for i in range(16,256-8, 8):
            self.game_objects.add(Boundary(self.game_objects, 0, i, 8, 8))
            self.game_objects.add(Boundary(self.game_objects, 256-8, i, 8, 8))

        self.events = []
        for event in [EventUp(), EventDown(), EventLeft(), EventRight()]:
            event.subscribe(monster)
            self.events.append(event)
        
        self.game_objects.score = 0
        self.game_state = GameState.PLAYING
    
    def update(self):
        if self.game_state == GameState.PLAYING:
            for obj in self.game_objects.objects:
                obj.reset()

            monster = self.game_objects[0]
            corpse = self.game_objects[1]
            if monster.collision(corpse.box):
                self.game_objects[1] = Corpse(self.game_objects, random.randint(16,240), random.randint(32,240))
                self.game_objects.score += 1
                self.game_objects.add(Enemy(self.game_objects, random.randint(16,256-16), 256-32))
        
            if pyxel.btn(pyxel.KEY_H):
                enemy = Enemy(self.game_objects, random.randint(16,256-16), 256-32)
                for e in self.events:
                    e.subscribe(enemy)
                self.game_objects.add(enemy)
            
            for event in self.events:
                event.trigger()
            
            for obj in self.game_objects.objects:
                obj.update()
            
            if len([e for e in self.game_objects.objects if isinstance(e, Enemy)]) <= 0:
                self.game_state = GameState.GAME_OVER
            if self.game_objects.score >= 10:
                self.game_state = GameState.WON
        else:
            if pyxel.btn(pyxel.KEY_N):
                self.new_game()


    def draw(self):
        pyxel.cls(0)
        if self.game_state == GameState.PLAYING:
            for obj in self.game_objects:
                obj.draw()

            pyxel.text(
                5,              # x-position of the text
                5,              # y position of the text
                str(f"Score {self.game_objects.score}"), # displayed text as string
                7               # text color
                )
            
            pyxel.text(
                50,             # x-position of the text
                5,              # y position of the text
                str(f"Enemies {len([e for e in self.game_objects.objects if isinstance(e, Enemy)])}"), # displayed text as string
                7               # text color
                )
        if self.game_state == GameState.WON:
            pyxel.text(
                90,
                120,
                str(f"Victory, press N for new game"),
                7
                )
        if self.game_state == GameState.GAME_OVER:
            pyxel.text(
                90,
                120,
                str(f"Game Over, press N for new game"),
                7
                )
App()