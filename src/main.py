import pygame as pg
from sprites import *
from ui import *
from sys import exit

pg.init()
pg.display.set_caption("Tanks")
clock = pg.time.Clock()

game = Game()

running = True
while running:
    clock.tick(FPS) 
    #gather events   
    events = pg.event.get()
    # check for the X button being pressed
    for event in events:        
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                
    game.update()
    game.draw()

pg.quit()
exit()