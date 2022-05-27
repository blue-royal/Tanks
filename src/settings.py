from matplotlib.ft2font import HORIZONTAL
import pygame as pg

import ctypes
user32 = ctypes.windll.user32

WIDTH = user32.GetSystemMetrics(0) # window width
HEIGHT = user32.GetSystemMetrics(1) # window height

FPS = 60

RESTARTBUFFER = 0.5

TANKSIZE = 20

TANKSPEED = 80
TANKROTATIONSPEED = 3

RELOADTIME = 0.25

TURRETWIDTH = 17
TURRETHEIGHT = 5
TURRETOFFSET = 8
TURRETROTATIONSPEED = 5
MAXBULLETS = 7

BULLETSPEED = 130
BULLETSIZE = 4
BULLETLIFESPAN = 4


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

ATTACKDISTANCE = 250
BASEPROXIMITY = 100
SHOTATDISTANCE = 100

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


screen = pg.display.set_mode((WIDTH, HEIGHT))