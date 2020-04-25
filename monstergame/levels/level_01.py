import random
from typing import List
from monstergame.utility_classes import Event
from monstergame.game_classes import Level, GameContainer, Boundary, TextBox, GameObject, Item


class Level01(Level):
    def __init__(self, game: GameContainer, x: int, y: int, width: int, height: int):
        self.door: List[GameObject] = []
        self.key: Item = []
        super().__init__(game, x, y, width, height)
    
    def setup(self):
        objects = []
        for i in range(0, self.box.h, 8):
            obj = Boundary(
                self.game,
                112,
                i,
                8,
                8,
                self.box.left_top_vector
            )
            objects.append(obj)
        
        for i in range(0, self.box.h, 8):
            obj = Boundary(
                self.game,
                self.box.w - 8,
                i,
                8,
                8,
                self.box.left_top_vector
            )
            self.door.append(obj)
        objects.extend(self.door)

        objects.append(
            TextBox(
                self.game, 10, 10, 85, parent=self.box.left_top_vector,
                line1="Welcome player", line2="this is MonsterGame")
        )

        objects.append(
            TextBox(
                self.game, 150, 10, 50, parent=self.box.left_top_vector,
                line1="Get the key", )
        )

        self.key = Item(self.game, 130, 5, 16, 0, self.box.left_top_vector)
        self.key.subscribe(self)
        objects.append(self.key)

        super().setup(
            *objects
        )
    
    def react(self, event: Event):
        if event is self.key:
            print("removing door")
            for obj in self.door:
                self.objects.remove(obj)
                self.game.objects.remove(obj)
            self.objects.remove(self.key)
            self.game.objects.remove(self.key)
            self.key.unsubscribe(self)

