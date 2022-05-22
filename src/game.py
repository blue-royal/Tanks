from turtle import width
from sprites import *
from settings import *
from ui import *
# Game class to control collisions and all bullets
# Level design files

def pauseGame():
    MenuScreen.state = MENU
    Game.counter = 0



class Game():
    counter = 0
    def __init__(self):
        
        level1 = {
            ENEMIES : [AI_Tank(400, 450, RED, [(600, 100), (600, 500), (100, 500), (100, 100)])],
            ENVIRONMENT : [Block(300, 300, 200, 50), Block(0, HEIGHT/2, 20, HEIGHT) , Block(WIDTH/2, 0, WIDTH + 10, 20)
                            , Block(WIDTH/2, HEIGHT, WIDTH + 20, 20), Block(WIDTH, HEIGHT/2, 20, HEIGHT + 20)],
            STARTPOS : [50, 50]
        }
        self.levels = [level1]
        
        self.pauseButton = Button(3, 3, 25, 25, (21, 21, 220), "P", 25, pauseGame)
        self.level = 1
        self.loadLevel()
        
    def run(self):
        if self.counter < RESTARTBUFFER * FPS:
            self.counter += 1
        else:
            self.update()
            self.draw()
    def loadLevel(self):
        currentLevel = self.levels[self.level-1]
        self.player = PlayerTank(currentLevel[STARTPOS][0], currentLevel[STARTPOS][1], BLUE)
        self.enemies = currentLevel[ENEMIES]
        self.env = currentLevel[ENVIRONMENT]
    def update(self):
        self.player.update(self.env)
        for enemy in self.enemies:
            enemy.update(self.player.x, self.player.y, self.env)
        self.pauseButton.update()
        Bullet.update(self.env)
    def draw(self):
        # render / draw sprites in correct order
        screen.fill(WHITE)
        for enemy in self.enemies:
            enemy.draw()
        self.player.draw()
        if self.env:
            for block in self.env:
                block.draw()
        Bullet.draw()
        
        self.pauseButton.draw()
        
        pg.display.flip()   