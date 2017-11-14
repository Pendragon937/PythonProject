import pygame
from pygame.locals import *

def main():
    pygame.init() #initializes pygame
    screen = pygame.display.set_mode((1000,1000))
    pygame.display.set_caption('Snake')

    background = pygame.Surface((100,100))
    background = background.convert()
    background.fill((0,100,100))

    # font = pygame.font.Font(None, 36)
    # text = font.render("Hello There", 1, (10, 10, 10))
    # textpos = text.get_rect()
    # textpos.centerx = background.get_rect().centerx
    # background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.display.flip() #updates screen


if __name__  == '__main__': main()