from sprites import *
from settings import *
from ui import *
from copy import deepcopy
# Game class to control collisions and all bullets
# Level design files

def pauseGame():
    MenuScreen.state = MENU
    Game.counter = 0


class Game():
    counter = 0
    def __init__(self):   
        level1 = {
            ENEMIES : [AI_Tank(WIDTH-50, HEIGHT/2, RED, [(WIDTH-50, HEIGHT/2), (WIDTH-100, HEIGHT/6), (WIDTH-100, 5*HEIGHT/6), (2*WIDTH/3, 50), (2*WIDTH/3, HEIGHT-50), (WIDTH/2, HEIGHT/2)]),
                       AI_Tank(WIDTH/2, HEIGHT/2, RED, [(WIDTH/2, HEIGHT/2), (WIDTH-150, HEIGHT/6), (WIDTH-150, 5*HEIGHT/6), (2*WIDTH/3, 100), (2*WIDTH/3, HEIGHT-100), (WIDTH/2, HEIGHT/2), (WIDTH/3, 100), (WIDTH/3, HEIGHT-100)])],
            ENVIRONMENT : [Block(WIDTH/4, HEIGHT/2, 50, 350), Block(3*WIDTH/4, HEIGHT/2, 50, 350), Block(WIDTH/2, HEIGHT/7, 50, 200), Block(WIDTH/2, 6*HEIGHT/7, 50, 200)],
            STARTPOS : [50, HEIGHT/2]
        }
        level2 = {
            ENEMIES : [AI_Tank(3*WIDTH/4, HEIGHT/4, RED, [(3*WIDTH/4, HEIGHT/4), (WIDTH-60, 60), (WIDTH/2, 50), (WIDTH-50, HEIGHT/2)]),
                       AI_Tank(WIDTH/4, 3*HEIGHT/4, RED, [(WIDTH/4, 3*HEIGHT/4), (60,HEIGHT-60), (50, HEIGHT/2), (WIDTH/2, HEIGHT - 50)]),
                       AI_Tank(WIDTH/2, HEIGHT-50, RED, [(WIDTH/2, HEIGHT-50), (4*WIDTH/5, HEIGHT-100), (4*WIDTH/5-40, 4*HEIGHT/5-40)]),
                       AI_Tank(WIDTH-50, HEIGHT/2, RED, [(WIDTH-50, HEIGHT/2), (WIDTH-100, 4*HEIGHT/5), (4*WIDTH/5+40, 4*HEIGHT/5+40)])],
            ENVIRONMENT : [Block(WIDTH/2, HEIGHT/2, 3*WIDTH/5, 75), Block(WIDTH/2, HEIGHT/2, 75, 3*HEIGHT/5)],
            STARTPOS : [WIDTH/4, HEIGHT/4]
        }
        
        self.levels = [level1, level2,level1]
        
        self.pauseButton = Button(3, 3, 25, 25, (50, 250, 220), "P", 20, 0, 0, pauseGame)
        self.level = 1
        self.loadLevel()
        
    def run(self):
        if Game.counter < RESTARTBUFFER * FPS:
            Game.counter += 1
        else:
            self.update()
            if MenuScreen.state == PLAY:
                self.draw()
            
    def loadLevel(self):
        Game.counter = 0
        if len(self.levels) == self.level:
            MenuScreen.state = MENU
            self.level = 1
        currentLevel = deepcopy(self.levels[self.level-1])
        self.player = PlayerTank(currentLevel[STARTPOS][0], currentLevel[STARTPOS][1], BLUE)
        self.enemies = currentLevel[ENEMIES]
        Bullet.clear()
        self.env = currentLevel[ENVIRONMENT]
        self.env.append(Block(0, HEIGHT/2, 20, HEIGHT))
        self.env.append(Block(WIDTH/2, 0, WIDTH + 10, 20))
        self.env.append(Block(WIDTH/2, HEIGHT, WIDTH + 20, 20))
        self.env.append(Block(WIDTH, HEIGHT/2, 20, HEIGHT + 20))
        
    def update(self):
        self.player.update(self.env)
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(self.player.x, self.player.y, self.env)
        self.pauseButton.update()
        Bullet.update(self.env)
        
        if PlayerTank.alive == False:
            self.loadLevel()
        elif self.checkWin():
            MenuScreen.state = MENU
            self.level += 1
            self.loadLevel()
            
    def draw(self):
        # render / draw sprites in correct order
        screen.fill(WHITE)
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw()
        self.player.draw()
        if self.env:
            for block in self.env:
                block.draw()
        Bullet.draw()
        
        self.pauseButton.draw()
        
        pg.display.flip()   
    
    def checkWin(self):
        for enemy in self.enemies:
            if enemy.alive:
                return False
        return True