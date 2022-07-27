from sprites import *
from settings import *
from ui import *
from copy import deepcopy

def pauseGame():
    MenuScreen.state = MENU
    Game.counter = 0


class Game():
    # to add a delay when starting the game
    counter = 0
    def __init__(self):  
        # Level creation data that is used to load levels 
        level1 = {
            ENEMIES : [AI_Tank(WIDTH-75, HEIGHT/2, RED, 
                               [(WIDTH-75, HEIGHT/2), (WIDTH-150, HEIGHT/6), (WIDTH-150, 5*HEIGHT/6), 
                                (2*WIDTH/3, 75), (2*WIDTH/3, HEIGHT-75), (WIDTH/2, HEIGHT/2)]),
                       AI_Tank(WIDTH/2, HEIGHT/2, RED, 
                               [(WIDTH/2, HEIGHT/2), (WIDTH-225, HEIGHT/6), (WIDTH-225, 5*HEIGHT/6), (2*WIDTH/3, 150), 
                                (2*WIDTH/3, HEIGHT-150), (WIDTH/2, HEIGHT/2), (WIDTH/3, 150), (WIDTH/3, HEIGHT-150)])],
            ENVIRONMENT : [Block(WIDTH/4, HEIGHT/2, 75, 525), Block(3*WIDTH/4, HEIGHT/2, 75, 525), 
                           Block(WIDTH/2, HEIGHT/7, 75, 300), Block(WIDTH/2, 6*HEIGHT/7, 75, 300)],
            STARTPOS : [75, HEIGHT/2]
        }
        level2 = {
            ENEMIES : [AI_Tank(3*WIDTH/4, HEIGHT/4, RED, [(3*WIDTH/4, HEIGHT/4), (WIDTH-90, 90), (WIDTH/2, 75), (WIDTH-75, HEIGHT/2)]),
                       AI_Tank(WIDTH/4, 3*HEIGHT/4, RED, [(WIDTH/4, 3*HEIGHT/4), (90,HEIGHT-90), (75, HEIGHT/2), (WIDTH/2, HEIGHT - 75)]),
                       AI_Tank(WIDTH/2, HEIGHT-75, RED, [(WIDTH/2, HEIGHT-75), (4*WIDTH/5, HEIGHT-150), (4*WIDTH/5-60, 4*HEIGHT/5-60)]),
                       AI_Tank(WIDTH-75, HEIGHT/2, RED, [(WIDTH-75, HEIGHT/2), (WIDTH-150, 4*HEIGHT/5), (4*WIDTH/5+60, 4*HEIGHT/5+60)])],
            ENVIRONMENT : [Block(WIDTH/2, HEIGHT/2, 3*WIDTH/5, 75), Block(WIDTH/2, HEIGHT/2, 75, 3*HEIGHT/5)],
            STARTPOS : [WIDTH/4, HEIGHT/4]
        }
        simpleLevel = {
            ENEMIES : [],
            ENVIRONMENT : [],
            STARTPOS : [WIDTH/2, HEIGHT/2]
        }
        
        
        oneEnemyLevel = {
            ENEMIES : [AI_Tank(WIDTH/2 + 300, HEIGHT/2, RED, [(WIDTH/2 + 300, HEIGHT/2)])],
            ENVIRONMENT : [],
            STARTPOS : [WIDTH/2-300, HEIGHT/2]
        }
        oneBlockLevel = {
            ENEMIES : [],
            ENVIRONMENT : [Block(WIDTH/2 + 150, HEIGHT/2, 200, 300)],
            STARTPOS : [WIDTH/2 - 150, HEIGHT/2]
        }
        ais = []
        for i in range(100):
            ais.append(AI_Tank(3*WIDTH/4 + (5*i), HEIGHT/4 + (5*i), RED, [(3*WIDTH/4 + (5*i), HEIGHT/4 + (5*i)), (WIDTH-90, 90 + (5*i)), (WIDTH/2 + (5*i), 75 + (5*i)), (WIDTH-75 - (5*i), HEIGHT/2 + (5*i))]))
        
        massAIlevel = {
            ENEMIES : ais ,
            ENVIRONMENT : [Block(WIDTH/2 - 500, HEIGHT/2, 100, HEIGHT- 200)],
            STARTPOS : [WIDTH/2 - 650, HEIGHT/2]
        }
        
        self.levels = [massAIlevel]
    # Takes a UI element Butto and allows the player to pause the game
        self.pauseButton = Button(4, 4, 37, 37, (50, 250, 220), "P", 30, 0, 0, pauseGame)
        self.level = 1
        self.loadLevel()
        
    def run(self):
        # Add a delay before starting the game
        if Game.counter < RESTARTBUFFER * FPS:
            Game.counter += 1
        else:
            self.update()
            if MenuScreen.state == PLAY:
                self.draw()
            
    def loadLevel(self):
        Game.counter = 0
        # If the last level is completed, restart the game
        if len(self.levels) == self.level:
            MenuScreen.state = MENU
            self.level = 1
        # load the latest level into the relevent variables
        currentLevel = deepcopy(self.levels[self.level-1])
        self.player = PlayerTank(currentLevel[STARTPOS][0], currentLevel[STARTPOS][1], BLUE)
        self.enemies = currentLevel[ENEMIES]
        Bullet.clear()
        self.env = currentLevel[ENVIRONMENT]
        self.env.append(Block(0, HEIGHT/2, 30, HEIGHT))
        self.env.append(Block(WIDTH/2, 0, WIDTH + 15, 30))
        self.env.append(Block(WIDTH/2, HEIGHT, WIDTH + 30, 30))
        self.env.append(Block(WIDTH, HEIGHT/2, 30, HEIGHT + 30))
        
    def update(self):
        #update the player, enemies, bullets and button objects
        self.player.update(self.env)
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(self.player.x, self.player.y, self.env)
        self.pauseButton.update()
        Bullet.update(self.env)
        
        # Check if the game is over or the level has been completed 
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
    
    # If no more enemies are alive then return true because the player has won
    def checkWin(self):
        # return False
        for enemy in self.enemies:
            if enemy.alive:
                return False
        return True