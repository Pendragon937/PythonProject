import os, pygame,math
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def load_image(name):
    path = os.path.join(main_dir, 'data', name)
    return pygame.image.load(path).convert()

class SpaceShip(object):
    def __init__(self,p1,p2,p3):
        SpaceShip.p1 = p1
        SpaceShip.p2 = p2
        SpaceShip.p3 = p3
    def draw(self,screen):
        pygame.draw.polygon(screen,RED,[self.p1,self.p2,self.p3])


def main():
    pygame.init() #initializes pygame
    screen = pygame.display.set_mode((1000,1000))
    pygame.display.set_caption('Asteroid')

    done = False
    clock = pygame.time.Clock()



    # Event loop
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        screen.fill(WHITE)
        ship = SpaceShip([500,500],[525,525],[475,525])
        ship.draw(screen)
        # pygame.draw.line(screen,RED,[500,500],[525,525],5)
        # pygame.draw.line(screen,RED,[500,500],[475,525],5)
        # pygame.draw.line(screen,RED,[525,525],[475,525],5)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__  == '__main__': main()