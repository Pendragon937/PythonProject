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
    def moveXY(self):
        self.rect.y += 2 * math.sin(math.radians(-1 * self.angle - 90))
        self.rect.x += 2 * math.cos(math.radians(-1 * self.angle - 90))



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

    def offScreen(self):
        if self.rect.y < -1 *self.image.get_height():
            return True
        elif self.rect.y > pygame.display.get_surface().get_height():
            return True
        elif self.rect.x < -1*self.image.get_width():
            return True
        elif self.rect.x > pygame.display.get_surface().get_width():
            return True
        else:
            return False
    def split(self):
        rx = self.rect.x
        ry = self.rect.y
        if self.ast_size == 'Big':
            self.ast_size = 'Medium'
            self.image = load_image('Asteroid2.png')
            self.rect = self.image.get_rect()
            self.rect.x = rx
            self.rect.y = ry
        elif self.ast_size == 'Medium':
            self.ast_size = 'Small'
            self.image = load_image('Asteroid3.png')
            self.rect = self.image.get_rect()
            self.rect.x = rx
            self.rect.y = ry
        else:
            return 'empty'


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('Bullet.png')
        self.rect = self.image.get_rect()
        self.angle = 0
    def update(self):
        self.rect.y += 5* math.sin(math.radians(-1*self.angle - 90))
        self.rect.x += 5* math.cos(math.radians(-1*self.angle - 90))

    def offScreen(self):
        if self.rect.y < -1 * self.image.get_height():
            return True
        elif self.rect.y > pygame.display.get_surface().get_height():
            return True
        elif self.rect.x < -1 * self.image.get_width():
            return True
        elif self.rect.x > pygame.display.get_surface().get_width():
            return True
        else:
            return False

def main():
    pygame.init() #initializes pygame
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption('Asteroid')

    done = False
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    shoot_sound = pygame.mixer.Sound('laser5.ogg')
    original = load_image('Ship.png')

    bullet_list = pygame.sprite.Group()
    asteroid_list = pygame.sprite.Group()

    ship = SpaceShip()
    ship.rect.x = 400
    ship.rect.y = 400
    screen.blit(ship.image,ship.rect)

    # for a in range(4):
    #     a = Asteroid('Big')
    ast = Asteroid('Big')
    ast.rect.x = 100
    ast.rect.y = 100
    asteroid_list.add(ast)
    asteroid_list.draw(screen)
    frame_count = 0
    frame_rate = 60
    start_time = 90
    pygame.display.flip()

    # Event loop
    while not done:
        #key events
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

        if keys[pygame.K_UP]:
            ship.moveXY()

        #update screen
        screen.fill(BLACK)
        screen.blit(ship.image,ship.rect)
        bullet_list.update()
        asteroid_list.update()

        #update timer      
        total_sec = frame_count // frame_rate
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "Time : {0:02}:{1:02}".format(minutes, seconds)
        text = font.render(output_string, True, BLACK)
        screen.blit(text, [250, 250])

        #asteroid, ship collision
        for a in asteroid_list:
            if pygame.sprite.collide_rect(a,ship):
                done = True
        if done:
            continue

        #bullet, asteroid collision
        for b in bullet_list:
            for a in asteroid_list:
                if pygame.sprite.collide_rect(b,a):
                    bullet_list.remove(b)
                    ast = a.split()
                    if ast == 'empty':
                        asteroid_list.remove(a)

        #bullet, asteroid off screen
        for b in bullet_list:
            if b.offScreen():
                bullet_list.remove(b)

        for a in asteroid_list:
            if a.offScreen():
                asteroid_list.remove(a)

                
        frame_count += 1
        bullet_list.draw(screen)
        asteroid_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__  == '__main__': main()
