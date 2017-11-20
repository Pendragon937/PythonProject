import os, pygame,math
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def load_image(name):
    path = os.path.join(main_dir, name)
    return pygame.image.load(path).convert()

    
def rot_center(image,angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('Ship.png')
        self.rect = self.image.get_rect()
        self.angle = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4,10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.angle = 0
    def update(self):
        self.rect.y += 5* math.sin(math.radians(-1*self.angle - 90))
        self.rect.x += 5* math.cos(math.radians(-1*self.angle - 90))

def main():
    pygame.init() #initializes pygame
    screen = pygame.display.set_mode((1000,1000))
    pygame.display.set_caption('Asteroid')

    done = False
    clock = pygame.time.Clock()
    original = load_image('Ship.png')
    bullet_list = pygame.sprite.Group()
    ship = SpaceShip()
    screen.fill(WHITE)
    ship.rect.x = 500
    ship.rect.y = 500
    screen.blit(ship.image,ship.rect)
    pygame.display.flip()

    # bull = Bullet()

    # Event loop
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ship.angle += 15
                    ship.image = rot_center(original,ship.angle)
                elif event.key == pygame.K_RIGHT:
                    ship.angle -= 15
                    ship.image = rot_center(original,ship.angle)
                elif event.key == pygame.K_SPACE:
                    bullet = Bullet()
                    bullet.angle = ship.angle
                    bullet.rect.x = ship.rect.x
                    bullet.rect.y = ship.rect.y
                    bullet_list.add(bullet)

        screen.fill(WHITE)
        screen.blit(ship.image,(500,500))

        bullet_list.update()
        bullet_list.draw(screen)
        Asteroid = load_image('Asteroid.png')
        screen.blit(Asteroid, (900,500))
        screen.blit(Asteroid, (100,500))
        screen.blit(Asteroid, (500,100))
        screen.blit(Asteroid, (500,900))
        # pygame.draw.line(screen,RED,[500,500],[525,525],5)
        # pygame.draw.line(screen,RED,[500,500],[475,525],5)
        # pygame.draw.line(screen,RED,[525,525],[475,525],5)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__  == '__main__': main()
