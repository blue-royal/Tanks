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
        
    def rotate(self, speed, env):
        tempRotation = self.rotation + (speed / FPS)
        tempRotation = tempRotation % (2 * pi)
        if not self.checkEnvironment(self.x, self.y, self.rotation, env):
            self.rotation = tempRotation
        
        
    def move(self, speed, env):
        delta_x = speed * cos(self.rotation) / FPS
        delta_y = speed * -sin(self.rotation) / FPS
        testX = self.x + delta_x
        testY = self.y + delta_y
        if not self.checkEnvironment(testX, testY, self.rotation, env):
            self.x += delta_x
            self.y += delta_y
    
    def checkEnvironment(self, x, y, rotation, env):
        points = rectanglePoints(x, y, TANKSIZE, TANKSIZE, rotation)
        for block in env:
            for point in points:
                if block.isPointInside(point[0], point[1]):
                    return True
        return False

        
    def draw(self):
        pg.draw.polygon(screen, self.colour, rectanglePoints(self.x, self.y, TANKSIZE, TANKSIZE, self.rotation))
        self.turret.draw()
        
    def bulletsCollide(self, x, y, radius):
        distance = ((self.x - x)**2 + (self.y - y)**2)**0.5
        if distance <= radius + TANKSIZE/2:
            return True
        else:
            return False
        
    
class PlayerTank(Tank):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
    def update(self, env):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rotate(TANKROTATIONSPEED, env) # change arbitrary value
        if keys[pg.K_d]:
            self.rotate(-TANKROTATIONSPEED, env) # change arbitrary value
        if keys[pg.K_w]:
            self.move(TANKSPEED, env) # change arbitrary value
        if keys[pg.K_s]:
            self.move(-TANKSPEED, env) # change arbitrary value
        self.turret.update(pg.mouse.get_pos())
        if pg.mouse.get_pressed()[0] == 1:
            self.turret.shoot()
            
        for bullet in Bullet.bullets:
            if self.bulletsCollide(bullet[1].x, bullet[1].y, BULLETSIZE):
                self.dead()
    def dead(self):
        print("The end")
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
        self.canReload = RELOADTIME * FPS
        
    def rotate(self, target):
        if (self.tank.x - target[0]) == 0:
            if self.tank.y - target[1] > 0:
                targetRotation = pi/2
            else:
                targetRotation = (3*pi)/2
        elif target[0] - self.tank.x >= 0:
            targetRotation = -atan((self.tank.y - target[1]) / (self.tank.x - target[0])) %(2*pi)
        else:
            targetRotation = (-atan((self.tank.y - target[1]) / (self.tank.x - target[0])) + pi)%(2*pi)
        
        # find the min of self.rotation - targetROtation and targetRotation - self.rotation both mod 2pi
        # then check if that difference is more than the rotation max speed, if not then set self.rotation = targetRotation
        # else increment self.rotation in the necessary direction and mod 2pi
        if (self.rotation - targetRotation) % (2*pi) > (targetRotation - self.rotation) % (2*pi):
            if (self.rotation - targetRotation) % (2*pi) < TURRETROTATIONSPEED/FPS:
                self.rotation = targetRotation
            else:
                self.rotation += TURRETROTATIONSPEED/FPS
        else:
            if (targetRotation - self.rotation) % (2*pi) < TURRETROTATIONSPEED/FPS:
                self.rotation = targetRotation
            else:
                self.rotation -= TURRETROTATIONSPEED/FPS
            
    
    def update(self, target):
        self.rotate(target)
        self.canReload += 1
    def shoot(self):
        if self.canReload >= RELOADTIME * FPS:
            startX = self.tank.x + (cos(self.rotation) * (TANKSIZE))
            startY = self.tank.y - (sin(self.rotation) * (TANKSIZE))
            Bullet(startX, startY, self.rotation)
            self.canReload = 0

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
        
        # If a bullet collides with a block get its hit direction
        for block in env:
            isColliding, dir = block.isCircleColliding(self.x, self.y, BULLETSIZE)
            if isColliding == True:
                # bounce the bullet depending on which wall of the block it hit
                if dir == VERTICAL:
                    self.rotation -= (2 * self.rotation) % (2*pi)
                if dir == HORIZONTAL:
                    self.rotation = ((self.rotation + pi) - (2 * self.rotation)) % (2*pi)
                    
        # Check if different two bullets collide and destroy them if they do
        for bullet in Bullet.bullets:
            if bullet[0] != self.ID:
                #Determine if they collide by checking if the distance between the centers less than the sum
                # of their radii
                if ((self.x - bullet[1].x)**2 + (self.y - bullet[1].y)**2)**0.5 < 2*BULLETSIZE:
                    bullet[1].delete()
                    self.delete()
                    break
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
            if bullet[0] == self.ID:
                Bullet.bullets.pop(i)
                break

class Block(GameObject):
    def __init__(self, x, y, width, height):
        GameObject.__init__(self, x, y)
        self.width, self.height = width, height
    def isPointInside (self, x, y): # check if a x and y point are both within the bounds of the rectangle
        if x > self.x - (self.width/2) and x < self.x + (self.width/2):
            if y > self.y - (self.height/2) and y < self.y + (self.height/2):
                return True
        return False
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
        self.update()
        self.draw()
    def nextLevel(self):
        pass
    def update(self):
        self.player.update(self.env)
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

