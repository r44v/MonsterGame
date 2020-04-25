import pyxel # type: ignore
import math
import random
from typing import List
from enum import Enum
from .config import Config
from .levels import level_01, level_02
from .game_classes import GameContainer, GameObject, Boundary, Corpse, Monster, Enemy, Player, Background, Level
from .game_events import EventUp, EventDown, EventLeft, EventRight, EventSpacebar
from .utility_classes import Box, Vector, Event, Utils


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
        self.game = GameContainer()
        self.game.playable_area = Box(0, 8 , Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT-8)
        self.events = [EventUp(), EventDown(), EventLeft(), EventRight(), EventSpacebar()]
        
        player = Player(self.game,
            int((self.game.playable_area.w / 2) - (Player.width / 2)),
            int((self.game.playable_area.h / 2) - (Player.height / 2))
            )
        
        self.game.set_player(player)

        self.levels: List[Level] = [
            level_01.Level01(
                self.game,
                self.game.playable_area.u,
                self.game.playable_area.v,
                self.game.playable_area.w,
                self.game.playable_area.h
            ),
            level_02.Level02(
                self.game,
                self.game.playable_area.u + self.game.playable_area.w,
                self.game.playable_area.v,
                self.game.playable_area.w,
                self.game.playable_area.h
            ),
            level_02.Level02(
                self.game,
                self.game.playable_area.u + self.game.playable_area.w * 2,
                self.game.playable_area.v,
                self.game.playable_area.w,
                self.game.playable_area.h
            )
        ]

        for i in range(3, 103):
            self.levels.append(level_02.Level02(
                self.game,
                self.game.playable_area.u + self.game.playable_area.w * i,
                self.game.playable_area.v,
                self.game.playable_area.w,
                self.game.playable_area.h
            ))

        for event in self.events:
            event.subscribe(player)
            for level in self.levels:
                event.subscribe(level)
    
    def update(self):
        player_radius_box = self.game.player.box.copy().grow(Config.COLLISION_MARGIN)
        self.game.near_objects.clear()
        for obj in self.game.objects:
            if Utils.point_in_box(obj.box.copy().move(obj.parent).center, player_radius_box):
                self.game.near_objects.append(obj)

        for event in self.events:
            event.trigger()

        if self.game.player.move_vector.x != 0:
            self.move_sideways(self.game.player.move_vector.x)
            self.game.player.move_vector.move_to(0, self.game.player.move_vector.y)
        
        self.game.player.update()
        
        for level in self.levels:
            level.update()
        
        for obj in self.game.objects:
            obj.update()
    
    def draw(self):
        pyxel.cls(0)

        pyxel.line(0, 7, Config.SCREEN_WIDTH, 7, 7)

        pyxel.blt(
            0,0,0,16,8,8,8,0
        )

        for level in self.levels:
            if level.loaded:
                level.draw()
        
        for obj in self.game.objects:
            obj.draw()
        
        self.game.player.draw()
    
    def move_sideways(self, x: int):
        if x == 0:
            return
        can_move = True
        player_moved_box = self.game.player.box.copy().move(Vector(x, 0))
        for obj in self.game.near_objects:
            if obj.collision(player_moved_box) and obj.is_wall:
                can_move = False
        
        if can_move:
            for level in self.levels:
                level.move(-1 * x)
            return
        
        if (x != 0):
            if x < 0:
                x += 1
            if x > 0:
                x -= 1
            self.move_sideways(x)

        
App()