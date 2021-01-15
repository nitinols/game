import pygame
import os
import sys
import math

pygame.init()
pygame.mixer.init()
size = width, height = 1300, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tachanka')
FPS = 50
screen_rect = (0, 0, width, height)

SPAWNENEMI = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNENEMI, 1000)

SPAWNENEMIBOSS = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNENEMI, 10000)
YELLOW = (255, 255, 0)

def terminate():
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


class ScreenFrame(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = (0, 0, width, height)


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удается загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


arrow_image = load_image("arrow.png")
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
all_sprites = pygame.sprite.Group()
arrow_group = SpriteGroup()
enemy_group = SpriteGroup()

class Arrow(Sprite):
    arrow = arrow_image
    arrow0 = []

    def __init__(self, pos):
        super().__init__(arrow_group)
        self.image = self.arrow
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_arrow(position):
    Arrow(position)

def defeat():
    size1 = 800, 500
    screen = pygame.display.set_mode(size1)
    #pygame.mixer.Sound('D:/data/sounds/losecombat.mp3').play()
    fon = pygame.transform.scale(load_image('gameover.jpg'), (800, 500))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.mixer.Sound('D:/data/sounds/losecombat.mp3').stop()
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #pygame.mixer.Sound('D:/data/sounds/losecombat.mp3').stop()
                return
            elif event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(False)
                create_arrow(pygame.mouse.get_pos())
        screen.blit(fon, (0, 0))
        arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
        arrow_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    size1 = 800, 500
    screen = pygame.display.set_mode(size1)
    #pygame.mixer.Sound('D:/data/sounds/trevor-morris-immortal-city.mp3').play(loops=-1)
    fon = pygame.transform.scale(load_image('fon.png'), size1)
    fon1 = pygame.transform.scale(load_image("fon2.png"), size1)
    screen.blit(fon, (0, 0))
    poss = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.mixer.Sound('D:/data/sounds/trevor-morris-immortal-city.mp3').stop()
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 570 <= event.pos[0] <= 700 and 130 <= event.pos[1] <= 180:
                    #pygame.mixer.Sound('D:/data/sounds/trevor-morris-immortal-city.mp3').stop()
                    return
            elif event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(False)
                create_arrow(pygame.mouse.get_pos())
                if 570 <= event.pos[0] <= 700 and 130 <= event.pos[1] <= 170:
                    if not poss:
                        #pygame.mixer.Sound('D:/data/sounds/gunshot-dryfir.mp3').play()
                        poss = True
                    screen.blit(fon1, (0, 0))
                    create_arrow(pygame.mouse.get_pos())
                else:
                    poss = False
                    screen.blit(fon, (0, 0))
        arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
        arrow_group.draw(screen)
        if not poss:
            all_sprites.update()
            screen.blit(fon, (0, 0))
            arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
            arrow_group.draw(screen)
            all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

class Enemi(Sprite):
    def __init__(self, hp, sp, damag, pos, x, y):
        super().__init__(enemy_group)
        self.hp = hp
        self.speed = sp
        self.damag = damag
        self.sizen = 90, 150

        self.image = pygame.transform.scale(load_image("monstr2.png"), self.sizen)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.rect.x = x
        self.rect.y = y


    def update(self, player):
        dx, dy = self.rect.x - player.rect.x, self.rect.y - player.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        if not self.rect.colliderect(screen_rect):
            self.kill()

size_hero = 80, 120
player_image = pygame.transform.scale(load_image("player3.png"), size_hero)
player_image1 = pygame.transform.rotate(player_image, 180)
tile_width = 60
tile_height = 100


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.heath = 100
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)
        print('-------')

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1])

    def get_damaged(self, damage):
        self.heath -= damage
        if self.heath <= 0:
            defeat()
            pygame.mixer.quit()
            pygame.mixer.init()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)




bullets = pygame.sprite.Group()
start_screen()
pygame.mixer.quit()
pygame.mixer.init()

running = True

screen = pygame.display.set_mode((1300, 700))
hero = Player(100, 200)
print('+++++++++++')
while running:
    for event in pygame.event.get():
        create_arrow(pygame.mouse.get_pos())
        if event.type == pygame.QUIT or hero.heath <= 0:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hero.shoot()
        if event.type == SPAWNENEMI:
            enem = Enemi(200, 2, 8, (100, 600), 100, 500)
    

    keys = pygame.key.get_pressed()
    x, y = hero.pos
    if keys[pygame.K_LEFT] and x > 15:
        hero.move(x - 2, y)
    if keys[pygame.K_RIGHT] and x < 1300 - 15:
        hero.move(x + 2, y)
    fon = pygame.transform.scale(load_image('fonmain.jpg'), (1300, 700))
    screen.blit(fon, (0, 0))

    intro_text = [f"Здоровье: {hero.heath}"]
    font = pygame.font.Font(None, 30)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 1150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    arrow_group.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[-1])
    hero_group.draw(screen)
    arrow_group.draw(screen)
    enemy_group.draw((screen))

    clock.tick(FPS)
    pygame.display.flip()

pygame.mixer.quit()
pygame.quit()