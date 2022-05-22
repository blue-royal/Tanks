from settings import *

class Text:
    def __init__(self, message, fontSize):
        myfont = pg.font.SysFont('Helvetica', fontSize)
        self.textsurface = myfont.render(message, True, (0, 0, 0))
    def draw(self, x, y):
        screen.blit(self.textsurface, (x, y))

class Button():
    def __init__(self, x, y, w, h, colour, message=None, fontSize = 40, action=None):
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.text = Text(message, fontSize)
        self.drawColour = colour
        self.normalColour = colour
        self.pressedColour = (colour[0] -15, colour[1] - 15, colour[2] - 15)
        self.action = action
        self.lastMouseState = False
    def draw(self):
        pg.draw.rect(screen, self.drawColour, pg.Rect(self.x, self.y, self.width, self.height))
        self.text.draw(self.x, self.y)
    def update(self):
        if pg.mouse.get_pressed()[0]:
            if self.lastMouseState == False:
                mousePos = pg.mouse.get_pos()
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
    def clicked(self):
        self.action()
        


class MenuScreen():
    state = MENU
    def __init__(self):
        self.title = Text("Tanks!", 50)
        self.playButton = Button(WIDTH/2 - 75, 200, 150, 75, (100, 200, 50), "Play", 50, playGame)
        self.quitButton = Button(WIDTH/2 - 75, 400, 150, 75, (100, 200, 50), "Quit", 50, quitGame)
    def update(self):
        self.playButton.update()
        self.quitButton.update()
    def draw(self):
        screen.fill(WHITE)
        self.playButton.draw()
        self.quitButton.draw()
        self.title.draw(WIDTH/2-20, 50)
        pg.display.flip()
    def run(self):
        self.update()
        self.draw()

def quitGame():
    MenuScreen.state = QUIT
def playGame():
    MenuScreen.state = PLAY