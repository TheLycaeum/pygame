import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Star,self).__init__()
        self.image = pygame.Surface((2,2))
        pygame.draw.circle(self.image, 
                           (128, 128, 200), 
                           (0,0),
                           2,
                           0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        x, y = self.rect.center
        if self.rect.center[1] > Y_MAX:
            self.rect.center = (x, 0)
        else:
            self.rect.center = (x, y + 1)

class BulletSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BulletSprite, self).__init__()
        self.image = pygame.Surface((10,10))
        for i in range(5,0,-1):
            color = 255.0 * float(i)/5
            pygame.draw.circle(self.image, 
                               (0, 0, color), 
                               (5,5),
                               i,
                               0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-25)

    def update(self):
        x, y = self.rect.center
        y -= 20
        self.rect.center = x, y
        if y <= 0:
            self.kill()
        
class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, x_pos, groups):
        super(EnemySprite, self).__init__()
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, 0)

        self.velocity = random.randint(3, 10)

        self.add(groups)

    def update(self):
        x, y = self.rect.center

        if y > Y_MAX:
            x, y = random.randint(0, X_MAX), 0
            self.velocity = random.randint(3, 10)
        else:
            x, y = x, y+ self.velocity

        self.rect.center = x, y

class StatusSprite(pygame.sprite.Sprite):
    def __init__(self, ship, groups):
        super(StatusSprite, self).__init__()
        self.image = pygame.Surface((X_MAX,30))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = 0, Y_MAX

        default_font = pygame.font.get_default_font()
        self.font = pygame.font.Font(default_font,20)

        self.ship = ship
        self.add(groups)

    def update(self):
        score = self.font.render("Health : {}".format(self.ship.health),True,(150, 50, 50))
        self.image.fill((0,0,0))
        self.image.blit(score,(0,0))

class ShipSprite(pygame.sprite.Sprite):
    def __init__(self, groups):
        super(ShipSprite, self).__init__()
        self.image = pygame.image.load("ship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (X_MAX/2, Y_MAX - 40)
        self.dx = self.dy = 0 
        self.firing = self.shot = False
        self.health = 100
        
        self.groups = groups
        

    def update(self):
        # Handle movement
        x, y = self.rect.center
        self.rect.center = x + self.dx, y + self.dy

        # Handle firing
        if self.firing:
            self.shot = BulletSprite(x, y)
            self.shot.add(self.groups)

        if self.health < 0:
            self.kill()

        

    def steer(self, direction, operation):
        v = 10
        if operation == START:
            if direction in (UP, DOWN):
                self.dy = {UP   : -v,
                           DOWN : v}[direction]

            if direction in (LEFT, RIGHT):
                self.dx = {LEFT  : -v,
                           RIGHT : v}[direction]

        if operation == STOP:
            if direction in (UP, DOWN):
                self.dy = 0
            if direction in (LEFT, RIGHT):
                self.dx = 0

    def shoot(self, operation):
        if operation == START:
            self.firing = True
        if operation == STOP:
            self.firing = False


def create_starfield(group):
    for i in range(100):
        x,y = random.randrange(X_MAX), random.randrange(Y_MAX)
        s = Star(x, y)
        s.add(group)


def main():
    pygame.font.init()
    screen = pygame.display.set_mode((X_MAX, Y_MAX), DOUBLEBUF)
    everything = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    empty = pygame.Surface((X_MAX, Y_MAX))
    clock = pygame.time.Clock()

    starfield = create_starfield(everything)

    ship = ShipSprite(everything)
    ship.add(everything)

    status = StatusSprite(ship, everything)

    deadtimer = 30

    for i in range(10):
        pos = random.randint(0, X_MAX)
        EnemySprite(pos, [everything, enemies])


    while True:
        clock.tick(30)
        # Check for input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_DOWN:  
                    ship.steer(DOWN, START)
                if event.key == K_LEFT:  
                    ship.steer(LEFT, START)
                if event.key == K_RIGHT: 
                    ship.steer(RIGHT, START)
                if event.key == K_UP:    
                    ship.steer(UP, START)
                if event.key == K_LCTRL:
                    ship.shoot(START)

            if event.type == KEYUP:
                if event.key == K_DOWN:  
                    ship.steer(DOWN, STOP)
                if event.key == K_LEFT:  
                    ship.steer(LEFT, STOP)
                if event.key == K_RIGHT: 
                    ship.steer(RIGHT, STOP)
                if event.key == K_UP:    
                    ship.steer(UP, STOP)
                if event.key == K_LCTRL:
                    ship.shoot(STOP)

        # Check for impact
        hit_ships = pygame.sprite.spritecollide(ship, enemies, True)
        for i in hit_ships:
            ship.health -= 15

        if ship.health < 0:
            if deadtimer:
                deadtimer -= 1
            else:
                sys.exit()
            

        # Update sprites
        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()

    

if __name__ == '__main__':
    main()

