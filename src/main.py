import pygame as pg
from sprites import *
from ui import *
from sys import exit

pg.init()
pg.display.set_caption("Tanks")
clock = pg.time.Clock()

test = PlayerTank(200, 200, BLUE)
testBlock = Block(300, 300, 200, 10)

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
    
    # update sprites
    test.update()
    # render / draw sprites in correct order
    screen.fill(WHITE)
    
    test.draw()
    testBlock.draw()
    
    pg.display.flip()       

pg.quit()
exit()