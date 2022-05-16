from settings import *

class GameObject():
    def __init__(self, x, y):
        self.x, self.y = x, y
    def draw():
        print("Override default draw function")

class Tank(GameObject):
    def __init__(self, x, y, colour):
        GameObject.__init__(self, x, y)
        self.colour = colour
    def draw():
        pass