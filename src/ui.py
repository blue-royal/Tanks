from settings import *

class Text:
    def __init__(self, message, fontSize):
        myfont = pg.font.SysFont('Helvetica', fontSize)
        self.textsurface = myfont.render(message, True, (0, 0, 0))
    def draw(self, x, y):
        screen.blit(self.textsurface, (x, y))

class Button():
    def __init__(self, x, y, w, h, colour, message=None, fontSize = 40, textOffsetX=0, textOffsetY=0, action=None):
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.text = Text(message, fontSize)
        self.drawColour = colour
        self.normalColour = colour
        self.hoverColour = (colour[0] -15, colour[1] - 15, colour[2] - 15)
        self.pressedColour = (colour[0] -30, colour[1] - 30, colour[2] - 30)
        self.action = action
        self.lastMouseState = False
        self.textOffset = [textOffsetX, textOffsetY]
    def draw(self):
        pg.draw.rect(screen, self.drawColour, pg.Rect(self.x, self.y, self.width, self.height))
        self.text.draw(self.x + self.textOffset[0], self.y + self.textOffset[1])
    def update(self):
        mousePos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            if self.lastMouseState == False:
                if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
                    if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
                        self.lastMouseState = True
                        self.clicked()
        else:
            self.lastMouseState = False
        if self.lastMouseState:
            self.drawColour = self.pressedColour
        else:
            self.drawColour = self.normalColour
        
        # If the mouse is just hovering the darken the colour
        if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
            if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
                self.drawColour = self.hoverColour
                
    def clicked(self):
        if self.action != None:
            self.action()
        


class MenuScreen():
    state = MENU
    def __init__(self):
        self.title = Text("Tanks!", 50)
        self.playButton = Button(WIDTH/2 - 250, 200, 500, 150, (100, 200, 50), "Play", 50, 220, 50, playGame)
        self.quitButton = Button(WIDTH/2 - 250, 450, 500, 150, (100, 200, 50), "Quit", 50, 220, 50, quitGame)
    def update(self):
        self.playButton.update()
        self.quitButton.update()
    def draw(self):
        screen.fill(WHITE)
        self.playButton.draw()
        self.quitButton.draw()
        self.title.draw(WIDTH/2-50, 50)
        pg.display.flip()
    def run(self):
        self.update()
        self.draw()

def quitGame():
    MenuScreen.state = QUIT
def playGame():
    MenuScreen.state = PLAY