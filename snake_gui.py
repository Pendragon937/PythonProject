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

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,ast_size):
        super().__init__()
        self.ast_size = ast_size
        if ast_size == 'Big':
            self.image = load_image('Asteroid.png')
        elif ast_size == 'Medium':
            self.image = load_image('Asteroid2.png')
        else:
            self.image = load_image('Asteroid3.png')
        self.rect = self.image.get_rect()
        self.xspeed = 5
        self.yspeed = 5

    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed


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
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption('Asteroid')

    done = False
    clock = pygame.time.Clock()
    original = load_image('Ship.png')
    screen.fill(WHITE)

    bullet_list = pygame.sprite.Group()
    asteroid_list = pygame.sprite.Group()
    sprite_list = pygame.sprite.Group()

    ship = SpaceShip()
    ship.rect.x = 400
    ship.rect.y = 400
    screen.blit(ship.image,ship.rect)

    # ast = Asteroid('Small')
    # ast.rect.x = 100
    # ast.rect.y = 100
    # asteroid_list.add(ast)
    # asteroid_list.draw(screen)

    pygame.display.flip()

    # Event loop
    while not done:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = Bullet()
                bullet.angle = ship.angle
                bullet.rect.x = ship.rect.x + (ship.image.get_width() / 2)
                bullet.rect.y = ship.rect.y
                bullet_list.add(bullet)

        if keys[pygame.K_LEFT]:
            ship.angle += 2
            ship.image = rot_center(original,ship.angle)
        elif keys[pygame.K_RIGHT]:
            ship.angle -= 2
            ship.image = rot_center(original,ship.angle)



        screen.fill(WHITE)
        screen.blit(ship.image,(400,400))

        bullet_list.update()
        asteroid_list.update()
        for b in bullet_list:
            if b.rect.y < -10:
                bullet_list.remove(b)
            elif b.rect.y > 1010:
                bullet_list.remove(b)
            elif b.rect.x > 1004:
                bullet_list.remove(b)
            elif b.rect.x < -4:
                bullet_list.remove(b)


        bullet_list.draw(screen)
        asteroid_list.draw(screen)
        # screen.blit(ast.image,(100,100))

        # ast = load_image('Asteroid.png')
        # screen.blit(ast, (400,500))
        # screen.blit(ast, (100,500))
        # screen.blit(ast, (500,100))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__  == '__main__': main()
