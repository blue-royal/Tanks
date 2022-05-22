import pygame as pg
from game import *
from ui import *
from sys import exit

# Set up pygame window
pg.init()
pg.display.set_caption("Tanks")
clock = pg.time.Clock()

# Initialise the game class
mainscreen = MenuScreen()
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
        # check if the escape  button is pressed end program if it is
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                
    # Entry point to the game  
    # game.run()
    if MenuScreen.state == MENU:
        mainscreen.run()
    elif MenuScreen.state == QUIT:
        running = False
    elif MenuScreen.state == PLAY:
        game.run()
# Delete window and stop executing program
pg.quit()
exit()