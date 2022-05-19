from settings import *
from math import sin, cos, pi, atan 

def rectanglePoints(x, y, w, h, rotation=0):
    p1 = ((((w * cos(rotation)) + (h * sin(rotation)))/2) + x, ((((h * cos(rotation)) + (-w * sin(rotation)))/2) + y))
    p2 = ((((-w * cos(rotation)) + (h * sin(rotation)))/2) + x, ((((h * cos(rotation)) + (w * sin(rotation)))/2) + y))
    p3 = ((((-w * cos(rotation)) + (-h * sin(rotation)))/2) + x, ((((-h * cos(rotation)) + (w * sin(rotation)))/2) + y))
    p4 = ((((w * cos(rotation)) + (-h * sin(rotation)))/2) + x, ((((-h * cos(rotation)) + (-w * sin(rotation)))/2) + y))
    
    return [p1, p2, p3, p4]


class GameObject():
    def __init__(self, x, y):
        self.x, self.y = x, y
    def draw():
        print("Override default draw function")

class Tank(GameObject):
    def __init__(self, x, y, colour):
        super().__init__(x, y)
        self.rotation = 0
        self.colour = colour
        self.turret = Turret(self)
    def rotate(self, speed):
        self.rotation += speed / FPS
        self.rotation = self.rotation % (2 * pi)
    def move(self, speed):
        delta_x = speed * cos(self.rotation) / FPS
        delta_y = speed * -sin(self.rotation) / FPS
        self.x += delta_x
        self.y += delta_y
    def draw(self):
        pg.draw.polygon(screen, self.colour, rectanglePoints(self.x, self.y, TANKSIZE, TANKSIZE, self.rotation))
        self.turret.draw()
        
    
class PlayerTank(Tank):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rotate(TANKROTATIONSPEED) # change arbitrary value
        if keys[pg.K_d]:
            self.rotate(-TANKROTATIONSPEED) # change arbitrary value
        if keys[pg.K_w]:
            self.move(TANKSPEED) # change arbitrary value
        if keys[pg.K_s]:
            self.move(-TANKSPEED) # change arbitrary value
        self.turret.update(pg.mouse.get_pos())
        if pg.mouse.get_pressed()[0] == 1:
            self.turret.shoot()
#
class AI_Tank(Tank):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
    def update(self):
        pass

class Turret():
    def __init__(self, tank):
        self.tank = tank
        self.rotation = self.tank.rotation
        
    def rotate(self, target):
        if (self.tank.x - target[0]) == 0:
            if self.tank.y - target[1] > 0:
                self.rotation = pi/2
            else:
                self.rotation = (3*pi)/2
        elif target[0] - self.tank.x >= 0:
            self.rotation = -atan((self.tank.y - target[1]) / (self.tank.x - target[0])) %(2*pi)
        else:
            self.rotation = (-atan((self.tank.y - target[1]) / (self.tank.x - target[0])) %(2*pi)) + pi
    
    def update(self, target):
        self.rotate(target)
    def shoot(self):
        Bullet(self.tank.x, self.tank.y, self.rotation)

    def draw(self):
        xOffset =  TURRETOFFSET * cos(self.rotation)
        yOffset = TURRETOFFSET * -sin(self.rotation)
        pg.draw.polygon(screen, BLACK, rectanglePoints(self.tank.x + xOffset, self.tank.y + yOffset, TURRETWIDTH, TURRETHEIGHT, self.rotation))

        

class Bullet(GameObject):
    bullets = []
    currentID = 0
    def __init__(self, x, y, rotation):
        super().__init__(x, y)
        if len(Bullet.bullets) == 0:
            self.ID = Bullet.currentID
            Bullet.currentID += 1
            Bullet.bullets = [[self.ID, self]]
        else:
            self.ID = Bullet.currentID
            Bullet.currentID += 1
            Bullet.bullets.append([self.ID, self])
        self.rotation = rotation
        self.lifetime = 0
        self.colour = GREEN
    def move(self, env):
        deltaX =  BULLETSPEED * cos(self.rotation) / FPS
        deltaY = BULLETSPEED * -sin(self.rotation) / FPS
        self.x += deltaX
        self.y += deltaY
        for block in env:
            isColliding, dir = block.isCircleColliding(self.x, self.y, BULLETSIZE)
            if isColliding == True:
                if dir == VERTICAL:
                    self.rotation -= (2 * self.rotation) % (2*pi)
                if dir == HORIZONTAL:
                    self.rotation = ((self.rotation + pi) - (2 * self.rotation)) % (2*pi)
    @staticmethod
    def update(env):
        for bullet in Bullet.bullets:
            bullet[1].lifetime += 1
            if bullet[1].lifetime > BULLETLIFESPAN * FPS:
                bullet[1].delete()
            bullet[1].move(env)
    @staticmethod
    def draw():
        for bullet in Bullet.bullets:
            pg.draw.circle(screen, bullet[1].colour, (bullet[1].x, bullet[1].y), BULLETSIZE)
    def delete(self):
        for i, bullet in enumerate(Bullet.bullets):
            if bullet[0] == bullet[1].ID:
                Bullet.bullets.pop(i)
                break

class Block(GameObject):
    def __init__(self, x, y, width, height):
        GameObject.__init__(self, x, y)
        self.width, self.height = width, height
    def isRectColliding (x, y, w, h): # where checkX and chackY are the center of the rectangle
        pass
    def isCircleColliding(self, x, y, radius):
        dir = None
        testX = x
        testY = y
        if self.x - (self.width / 2) > x:
            testX = self.x - (self.width / 2)
            dir = HORIZONTAL
        elif self.x + (self.width / 2) < x:
            testX = self.x + (self.width / 2)
            dir = HORIZONTAL
        
        if self.y - (self.height / 2) > y:
            testY = self.y - (self.height / 2)
            dir = VERTICAL
        elif self.y + (self.height / 2) < y:
            testY = self.y + (self.height / 2)
            dir= VERTICAL
        
        distance = ((testX - x)**2 + (testY - y)**2)**0.5
        if distance <= radius:
            return (True, dir)
        else:
            return (False, dir)
        
    def draw(self):
        pg.draw.polygon(screen, ORANGE, rectanglePoints(self.x, self.y, self.width, self.height))

# Game class to control collisions and all bullets
# Level design files

class Game():
    def __init__(self):
        self.player = PlayerTank(200, 200, BLUE)
        self.env = [Block(300, 300, 200, 50)]
    def run(self):
        pass
    def nextLevel(self):
        pass
    def update(self):
        self.player.update()
        Bullet.update(self.env)
    def draw(self):
        # render / draw sprites in correct order
        screen.fill(WHITE)
        
        self.player.draw()
        if self.env:
            for block in self.env:
                block.draw()
        Bullet.draw()
        
        pg.display.flip()   

