from settings import *
from math import sin, cos, pi, atan

def rectanglePoints(x, y, w, h, rotation):
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

class AI_Tank(Tank):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
    def update(self):
        pass

class Turret():
    def __init__(self, tank):
        self.tank = tank
        self.rotation = self.tank.rotation
        self.bullets = []
        
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
        for bullet in self.bullets:
            bullet.update()
        self.rotate(target)
    def shoot(self):
        self.bullets.append(Bullet(self.tank.x, self.tank.y, self.rotation))
    def draw(self):
        xOffset =  TURRETOFFSET * cos(self.rotation)
        yOffset = TURRETOFFSET * -sin(self.rotation)
        pg.draw.polygon(screen, BLACK, rectanglePoints(self.tank.x + xOffset, self.tank.y + yOffset, TURRETWIDTH, TURRETHEIGHT, self.rotation))
        for bullet in self.bullets:
            bullet.draw()
        

class Bullet(GameObject):
    def __init__(self, x, y, rotation):
        super().__init__(x, y)
        self.rotation = rotation
        self.lifetime = 0
        self.colour = GREEN
    def move(self):
        deltaX =  BULLETSPEED * cos(self.rotation) / FPS
        deltaY = BULLETSPEED * -sin(self.rotation) / FPS
        self.x += deltaX
        self.y += deltaY
    def update(self):
        self.lifetime += 1
        if self.lifetime > BULLETLIFESPAN * FPS:
            self.delete()
        self.move()
    def draw(self):
        pg.draw.circle(screen, self.colour, (self.x, self.y), BULLETSIZE)
    def delete(self):
        self.colour = RED

class Block(GameObject):
    def __init__(self, x, y, width, height):
        GameObject.__init__(self, x, y)
        self.width, self.height = width, height
    def isRectColliding (x, y, w, h): # where checkX and chackY are the center of the rectangle
        pass
    def isCircleColliding(x, y, radius):
        pass
    def draw(self):
        pg.draw.rect(screen, ORANGE, pg.Rect(self.x, self.y, self.width, self.height))
    def distance(x1, y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5