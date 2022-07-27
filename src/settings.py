import pygame as pg
# Used to get screen dimensions
import ctypes
user32 = ctypes.windll.user32

WIDTH = user32.GetSystemMetrics(0) # window width
HEIGHT = user32.GetSystemMetrics(1) # window height

# Game control constants
FPS = 60
RESTARTBUFFER = 0.5

# Tank constants
TANKSIZE = 30

TANKSPEED = 120
TANKROTATIONSPEED = 3

RELOADTIME = 0.25

# Turret constants
TURRETWIDTH = 25.5
TURRETHEIGHT = 7.5
TURRETOFFSET = 12
TURRETROTATIONSPEED = 5
MAXBULLETS = 7

# Bullet constants
BULLETSPEED = 195
BULLETSIZE = 6
BULLETLIFESPAN = 4

# constants used in collision detection for readability
VERTICAL = 0
HORIZONTAL = 1

# Level constants
ENEMIES = 1
ENVIRONMENT = 2
STARTPOS = 3

# AI Tank states

ATTACK_EVADE = 0
CHASE_BLOCK = 1
SEARCH = 2

ATTACKDISTANCE = 375
BASEPROXIMITY = 150
SHOTATDISTANCE = 150

#Testing colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# MENU states
MENU = 0
QUIT = 1
PLAY = 2


screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)