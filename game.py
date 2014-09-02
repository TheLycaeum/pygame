import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN

X_MAX = 800
Y_MAX = 600

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

        # Update sprites
        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()

    

if __name__ == '__main__':
    main()

