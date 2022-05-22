from settings import *
from math import sin, cos, pi, atan 
from random import shuffle

# Apply rotation matrix of a given rotation to the given width and height then add the center of rotation
def rectanglePoints(x, y, w, h, rotation=0):
    p1 = ((((w * cos(rotation)) + (h * sin(rotation)))/2) + x, ((((h * cos(rotation)) + (-w * sin(rotation)))/2) + y))
    p2 = ((((-w * cos(rotation)) + (h * sin(rotation)))/2) + x, ((((h * cos(rotation)) + (w * sin(rotation)))/2) + y))
    p3 = ((((-w * cos(rotation)) + (-h * sin(rotation)))/2) + x, ((((-h * cos(rotation)) + (w * sin(rotation)))/2) + y))
    p4 = ((((w * cos(rotation)) + (-h * sin(rotation)))/2) + x, ((((-h * cos(rotation)) + (-w * sin(rotation)))/2) + y))
    # Returns points as tuples
    return [p1, p2, p3, p4]

# Every game object requires an x, y position and a draw and update function function
class GameObject():
    def __init__(self, x, y):
        self.x, self.y = x, y
    def update():
        print("please overide this update funciton")
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
        # Check if rotation causes a collision with any blocks
        if not self.checkEnvironment(self.x, self.y, self.rotation, env):
            # update the rotation to be the newly calculated
            self.rotation = tempRotation
        
        
    def move(self, speed, env):
        # calculate the change in x, y co-ordinates using the rotation
        delta_x = speed * cos(self.rotation) / FPS
        delta_y = speed * -sin(self.rotation) / FPS
        # store new coordinate in temporary variale to check for collisions with any blocks
        tempX = self.x + delta_x
        tempY = self.y + delta_y
        if not self.checkEnvironment(tempX, tempY, self.rotation, env):
            self.x += delta_x
            self.y += delta_y
    
    # The function that determines if any tank vertices are inside the block
    def checkEnvironment(self, x, y, rotation, env):
        # get corners of the tanks coordinates
        points = rectanglePoints(x, y, TANKSIZE, TANKSIZE, rotation)
        for block in env:
            for point in points:
                # check if those points are inside the block 
                if block.isPointInside(point[0], point[1]):
                    return True
        # if no points are inside the blocks then return false
        return False

    # draw the tank using its corner co-ordinates and after the tank is drawn, draw the turret
    def draw(self):
        pg.draw.polygon(screen, self.colour, rectanglePoints(self.x, self.y, TANKSIZE, TANKSIZE, self.rotation))
        self.turret.draw()
    
    # check if any of the bullets are colliding with the tank
    def bulletsCollide(self, x, y, radius):
        # model the tank as a circle for collision detection purposes
        distance = ((self.x - x)**2 + (self.y - y)**2)**0.5
        if distance <= radius + TANKSIZE/2:
            return True
        else:
            return False
        
    
class PlayerTank(Tank):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
    def update(self, env):
        # get key event information to determine who to move and orient tank
        # when WASD keys are pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rotate(TANKROTATIONSPEED, env) 
        if keys[pg.K_d]:
            self.rotate(-TANKROTATIONSPEED, env)
        if keys[pg.K_w]:
            self.move(TANKSPEED, env) 
        if keys[pg.K_s]:
            self.move(-TANKSPEED, env) 
        #update turret position based on the mouse position
        self.turret.update(pg.mouse.get_pos())
        # shoot if the right mouse button is pressed
        if pg.mouse.get_pressed()[0] == 1:
            self.turret.shoot()
            
        # Check if any bullets are colliding with the tank
        for bullet in Bullet.bullets:
            if self.bulletsCollide(bullet[1].x, bullet[1].y, BULLETSIZE):
                bullet[1].delete()
                # if a collision has occured, then the tank is destroyed
                self.dead()
    # if player tank is dead trigger, the death screen
    def dead(self):
        print("The end")
        # trigger death screen
#
class AI_Tank(Tank):
    def __init__(self, x, y, colour, bases):
        super().__init__(x, y, colour)
        self.targetPosX = bases[0][0]
        self.targetPosY = bases[0][1]
        self.bases = bases
        self.newTargetPos = False
        self.wasInProimity = False
    
    # Run AI
    def update(self, playerX, playerY, env):
        # If bullet collides with AI tank the destroy the tank 
        state = self.chooseState(playerX, playerY, env)
        if state == ATTACK_EVADE:
            self.newTargetPos = True
            # aim at player and shoot
            if self.turret.update((playerX, playerY)):
                self.turret.shoot()
            # move out of the way of incoming bullets
            
        if state == CHASE_BLOCK:
            self.newTargetPos = True
            self.rotate((playerX, playerY))
            self.move(TANKSPEED, env)
            
        if state == SEARCH:
            # if the distance to the target position is less than 50 pixels pick a new aim
            if (self.x - self.targetPosX) **2 + (self.y - self.targetPosY)**2 < BASEPROXIMITY**2:
                if not self.wasInProimity:
                    self.newTargetPos = True
                self.wasInProimity = True
            else:
                self.wasInProimity = False
                
            
            # set a new target position that is in the line of sight
            if self.newTargetPos == True:
                self.newTargetPos = False
                # shuffle possible bases so a new base is always random
                shuffle(self.bases)
                for base in self.bases:
                    if self.lineOfSight(base[0], base[1], env) and not (self.targetPosX == base[0] and self.targetPosY == base[1]):
                        self.targetPosX = base[0]
                        self.targetPosY = base[1]
                        break
            # rotate towards new position
            self.rotate((self.targetPosX, self.targetPosY))
            # move forwards or backwards, whichever's quicker
            self.move(TANKSPEED, env)
        
        for bullet in Bullet.bullets:
            if self.bulletsCollide(bullet[1].x, bullet[1].y, BULLETSIZE):
                bullet[1].delete()
                self.dead()
                
    def lineOfSight(self, targetX, targetY, env):
        #line of sight calc is a possible point of performance issues
        dirVecX = targetX - self.x
        dirVecY = targetY - self.y
        # normalise direction vector
        magnitude = (dirVecX**2 + dirVecY**2)**0.5
        dirVecX = dirVecX/magnitude
        dirVecY = dirVecY/magnitude
        lineOfSight = True
        t = 1
        # iterate through each pixel position on the line and check if it collides inside a block
        while t < magnitude:
            for block in env:
                if block.isPointInside(dirVecX*t + self.x, dirVecY * t + self.y):
                    lineOfSight = False
                    break
            t += 1
        return lineOfSight
    
    def chooseState(self, playerX, playerY, env):
        #Check if there is a line of sight to the player tank
        if self.lineOfSight(playerX, playerY, env):
            if (playerX - self.x)**2 + (playerY - self.y) **2 < ATTACKDISTANCE **2:
                return ATTACK_EVADE
            else: return CHASE_BLOCK
        else: return SEARCH
            
    def rotate(self, target):
        # find the target rotation based on the mouse position
        if (self.x - target[0]) == 0:
            if self.y - target[1] > 0:
                targetRotation = pi/2
            else:
                targetRotation = (3*pi)/2
        elif target[0] - self.x >= 0:
            targetRotation = -atan((self.y - target[1]) / (self.x - target[0])) %(2*pi)
        else:
            targetRotation = (-atan((self.y - target[1]) / (self.x - target[0])) + pi)%(2*pi)
        
        # Check which direction 
        if (self.rotation - targetRotation) % (2*pi) < (targetRotation - self.rotation) % (2*pi):
            if (self.rotation - targetRotation) % (2*pi) <= TANKROTATIONSPEED/FPS:
                self.rotation = targetRotation
                return True
            else:
                self.rotation -= TANKROTATIONSPEED/FPS
                return False
        else:
            if (targetRotation - self.rotation) % (2*pi) <= TANKROTATIONSPEED/FPS:
                self.rotation = targetRotation
                return True
            else:
                self.rotation += TANKROTATIONSPEED/FPS
                return False
            
    def dead(self):
        print("I died")

# Controls shooting and managing the bullets for every tank
class Turret():
    def __init__(self, tank):
        self.tank = tank
        self.rotation = self.tank.rotation
        self.canReload = RELOADTIME * FPS
    
    # Rotate the turret towards the mouse with a maximum rotation speed
    # Return true if aiming directly at target
    def rotate(self, target):
        # find the target rotation based on the mouse position
        if (self.tank.x - target[0]) == 0:
            if self.tank.y - target[1] > 0:
                targetRotation = pi/2
            else:
                targetRotation = (3*pi)/2
        elif target[0] - self.tank.x >= 0:
            targetRotation = -atan((self.tank.y - target[1]) / (self.tank.x - target[0])) %(2*pi)
        else:
            targetRotation = (-atan((self.tank.y - target[1]) / (self.tank.x - target[0])) + pi)%(2*pi)
        
        # Check which direction 
        if (self.rotation - targetRotation) % (2*pi) < (targetRotation - self.rotation) % (2*pi):
            if (self.rotation - targetRotation) % (2*pi) <= TURRETROTATIONSPEED/FPS:
                self.rotation = targetRotation
                return True
            else:
                self.rotation -= TURRETROTATIONSPEED/FPS
                return False
        else:
            if (targetRotation - self.rotation) % (2*pi) <= TURRETROTATIONSPEED/FPS:
                self.rotation = targetRotation
                return True
            else:
                self.rotation += TURRETROTATIONSPEED/FPS
                return False
            
    
    def update(self, target):
        self.canReload += 1
        return self.rotate(target)
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



