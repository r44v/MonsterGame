import random
from monstergame.game_classes import Level, GameContainer, Boundary


class Level02(Level):
    def __init__(self, game: GameContainer, x: int, y: int, width: int, height: int):
        super().__init__(game, x, y, width, height)
    
    def setup(self):
        objects = []
        
        for x in range(0, self.box.w, 32):
            obj = Boundary(
                    self.game,
                    x,
                    0,
                    8,
                    8,
                    self.box.left_top_vector
                )
            objects.append(obj)

            skip = random.randint(0,3)
            for y_step in range(4):
                if y_step == skip:
                    continue
                amount = 4
                objects.extend(
                    self.create_vertical_bounderies(amount, x , 8 + y_step * amount * 8)
                )
        super().setup(
            *objects
        )
    
    def create_vertical_bounderies(self, amount, x, y):
        objects = []
        for i in range(amount):
            obj = Boundary(
                self.game,
                x,
                y + (8 * i),
                8,
                8,
                self.box.left_top_vector
            )
            objects.append(obj)
        return objects
