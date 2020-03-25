import pyxel # type: ignore
import math
import random
from .config import Config
from .game_classes import GameContainer, GameObject, Boundary, Corpse, Monster, Enemy
from .game_events import EventUp, EventDown, EventLeft, EventRight
from .utility_classes import Box, Vector, Event


"""
TODO

- [ ] GameContainer has collisions list for each object
- [ ] User collission detected only for used movement
"""

class App:
    def __init__(self):
        pyxel.init(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        pyxel.load("assets.pyxres")

        self.game_objects = GameContainer()
        monster = Monster(self.game_objects, 100, 100)
        self.game_objects.add(monster)
        self.game_objects.add(Corpse(self.game_objects, random.randint(10,246), random.randint(10,246)))
        self.game_objects.add(Corpse(self.game_objects, 248,1))
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

        pyxel.run(self.update, self.draw)
    
    def update(self):
        for obj in self.game_objects.objects:
            obj.reset()

        # Well yes this is bogus logic    
        monster = self.game_objects[0]
        for corpse in self.game_objects[1:3]:
            if monster.collision(corpse.box):
                self.game_objects[1] = Corpse(self.game_objects, random.randint(16,256-16), random.randint(32,256-16))
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

    def draw(self):
        pyxel.cls(0)
        
        for obj in self.game_objects:
            obj.draw()

        pyxel.text(
            5,              # x-position of the text
            5,              # y position of the text
            str(f"Score {self.game_objects.score}"), # displayed text as string
            7               # text color
            )

App()