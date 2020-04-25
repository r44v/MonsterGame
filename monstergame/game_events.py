import pyxel # type: ignore
from .utility_classes import Event, EventObserver

class EventUp(Event):
    def __init__(self):
        super().__init__()
    
    def trigger(self):
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.notify()

class EventDown(Event):
    def __init__(self):
        super().__init__()
    
    def trigger(self):
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.notify()

class EventLeft(Event):
    def __init__(self):
        super().__init__()
    
    def trigger(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.notify()

class EventRight(Event):
    def __init__(self):
        super().__init__()
    
    def trigger(self):
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.notify()

class EventSpacebar(Event):
    def __init__(self):
        super().__init__()
    
    def trigger(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            self.notify()