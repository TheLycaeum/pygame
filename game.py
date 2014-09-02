import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, K_LEFT, K_UP, K_RIGHT

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4

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

    def update(self):
        pass

    def move(self, direction):
        v = 1
        dx, dy = {UP : (0, -v),
                  DOWN : (0, v),
                  LEFT : (-v, 0),
                  RIGHT : (v, 0)}[direction]

        x, y = self.rect.center
        self.rect.center = x + dx, y + dy


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
                    ship.move(DOWN)
                if event.key == K_LEFT:  
                    ship.move(LEFT)
                if event.key == K_RIGHT: 
                    ship.move(RIGHT)
                if event.key == K_UP:    
                    ship.move(UP)

            

        # Update sprites
        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()

    

if __name__ == '__main__':
    main()

