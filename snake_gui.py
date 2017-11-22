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
        self.xspeed = 1
        self.yspeed = 1

    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('Bullet.png')
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
    shoot_sound = pygame.mixer.Sound('laser5.ogg')
    original = load_image('Ship.png')

    bullet_list = pygame.sprite.Group()
    asteroid_list = pygame.sprite.Group()

    ship = SpaceShip()
    ship.rect.x = 400
    ship.rect.y = 400
    screen.blit(ship.image,ship.rect)

    ast = Asteroid('Big')
    ast.rect.x = 100
    ast.rect.y = 100
    asteroid_list.add(ast)
    asteroid_list.draw(screen)

    pygame.display.flip()

    # Event loop
    while not done:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shoot_sound.play()
                bullet = Bullet()
                bullet.angle = ship.angle
                bullet.rect.x = ship.rect.x + (ship.image.get_width() / 2)
                bullet.rect.y = ship.rect.y + (ship.image.get_width() / 2)
                bullet_list.add(bullet)

        if keys[pygame.K_LEFT]:
            ship.angle += 2
            ship.image = rot_center(original,ship.angle)
        elif keys[pygame.K_RIGHT]:
            ship.angle -= 2
            ship.image = rot_center(original,ship.angle)

        screen.fill(BLACK)
        screen.blit(ship.image,ship.rect)
        bullet_list.update()
        asteroid_list.update()

        for a in asteroid_list:
            if pygame.sprite.collide_rect(a,ship):
                done = True
        if done:
            continue

        for b in bullet_list:
            for a in asteroid_list:
                if pygame.sprite.collide_rect(b,a):
                    bullet_list.remove(b)
                    if a.ast_size == 'Big':
                        rx = a.rect.x
                        ry = a.rect.y
                        a.ast_size = 'Medium'
                        a.image = load_image('Asteroid2.png')
                        a.rect = a.image.get_rect()
                        a.rect.x = rx
                        a.rect.y = ry
                    elif a.ast_size == 'Medium':
                        rx = a.rect.x
                        ry = a.rect.y
                        a.ast_size = 'Small'
                        a.image = load_image('Asteroid3.png')
                        a.rect = a.image.get_rect()
                        a.rect.x = rx
                        a.rect.y = ry
                    else:
                        asteroid_list.remove(a)

        for b in bullet_list:
            if b.rect.y < -10:
                bullet_list.remove(b)
            elif b.rect.y > 810:
                bullet_list.remove(b)
            elif b.rect.x > 810:
                bullet_list.remove(b)
            elif b.rect.x < -10:
                bullet_list.remove(b)

        bullet_list.draw(screen)
        asteroid_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__  == '__main__': main()
