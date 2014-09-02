import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, K_LEFT, K_UP, K_RIGHT, KEYUP

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
            self.rect.center = (x, y + 5)
                           

class ShipSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(ShipSprite, self).__init__()
        self.image = pygame.image.load("ship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (X_MAX/2, Y_MAX - 40)
        self.dx = self.dy = 0 

    def update(self):
        x, y = self.rect.center
        self.rect.center = x + self.dx, y + self.dy

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



def create_starfield(group):
    for i in range(100):
        x,y = random.randrange(X_MAX), random.randrange(Y_MAX)
        s = Star(x, y)
        s.add(group)
        


def main():
    screen = pygame.display.set_mode((X_MAX, Y_MAX), DOUBLEBUF)
    everything = pygame.sprite.Group()
    empty = pygame.Surface((X_MAX, Y_MAX))
    clock = pygame.time.Clock()

    starfield = create_starfield(everything)

    ship = ShipSprite()
    ship.add(everything)

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

            if event.type == KEYUP:
                if event.key == K_DOWN:  
                    ship.steer(DOWN, STOP)
                if event.key == K_LEFT:  
                    ship.steer(LEFT, STOP)
                if event.key == K_RIGHT: 
                    ship.steer(RIGHT, STOP)
                if event.key == K_UP:    
                    ship.steer(UP, STOP)

            

        # Update sprites
        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()

    

if __name__ == '__main__':
    main()

