import pygame
import random

from pygame.sprite import Sprite


from pygame.locals import (
    RLEACCEL, 
    K_UP,
    K_DOWN,
    KEYDOWN,
    K_SPACE,
    QUIT, 
    KEYDOWN, 
    K_z,
    K_q,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0,0,0)

class Utils():

    @staticmethod
    def message_display(text):
        text_font = pygame.font.Font('freesansbold.ttf', 65)
        text_surface = text_font.render(text, True, BLACK)   
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        screen.blit(text_surface, text_rect)

        pygame.display.update() 


class Cloud(Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("assets/Cloud.png").convert()
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(-100, -20),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(5, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.kill()


class Enemy(Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("assets/missile.png").convert()
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(-100, -20),
                random.randint(5, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 8)

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

class Bomb(Sprite):

    def __init__(self, start_x, start_y, color):
        super(Bomb, self).__init__()
        self.surf = pygame.Surface((5, 3))
        self.surf.fill(pygame.Color(color))
        self.rect = self.surf.get_rect(
            center=(start_x, start_y)
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.left < 0:
            self.kill()

class Player(Sprite):
        
    def __init__(self):
        super(Player, self).__init__()  
        self.surf = pygame.image.load("assets/jet.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    def update(self, pressed_keys):

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
    def get_position(self):
        return (self.rect.left, self.rect.top)

pygame.init()

pygame.mixer.music.load("sounds\Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

move_up_sound = pygame.mixer.Sound("sounds\Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("sounds\Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("sounds\Collision.ogg")
explosion_sound = pygame.mixer.Sound("sounds\Explosion.wav")

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 300)

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bombs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

clock = pygame.time.Clock()
button = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT - 100, 60, 40)
while running:

    for event in pygame.event.get():
        pressed_keys = pygame.key.get_pressed()        
        if event.type == pygame.QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        
        elif event.type == KEYDOWN:
            #We will fire from right wing
            if pressed_keys[K_q]:
                # Create the new Bomb and add it to sprite groups
                pos_x, pos_y = player.get_position()
                new_bomb = Bomb(pos_x + 25, pos_y + 11, "red")
                bombs.add(new_bomb)
                all_sprites.add(new_bomb)
            elif pressed_keys[K_z]:
                #lets fire from left wing
                pos_x, pos_y = player.get_position()
                new_bomb = Bomb(pos_x + 25, pos_y + 35, "yellow")
                bombs.add(new_bomb)
                all_sprites.add(new_bomb)
                
    player.update(pressed_keys)
    
    enemies.update()
    clouds.update()
    bombs.update()

    screen.fill((135, 206, 250))
    pygame.draw.rect(screen, (30, 30, 30), button)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.groupcollide(enemies, bombs, True, True):
        explosion_sound.play()
    
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        Utils.message_display("It's Over!!")
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()