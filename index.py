import pygame
from pygame.locals import *
import random

pygame.init()

#plays music
pygame.mixer.init()
pygame.mixer.music.load('assets/audio/background_music.flac')
pygame.mixer.music.set_volume(0.5)
hit = pygame.mixer.Sound('assets/audio/hit.wav')
hit.set_volume(1.0)
pygame.mixer.music.play(-1)

# fps 
clock = pygame.time.Clock()
fps = 60

# screen size
screen = pygame.display.set_mode((1280, 720))

# title of the game when program starts
pygame.display.set_caption('City Runner')

# stores background and floor img in a var as well as sets scroll speed
floor_scroll = 0
scroll_speed = 400 
bg = pygame.image.load('assets/img/background/a.webp')
floor = pygame.image.load('assets/img/background/road.gif')

# Stretch the floor image to fit the screen width
floor_width = 1280
floor_height = 100
floor = pygame.transform.scale(floor, (floor_width, floor_height))

# game Var
enemy_freq_min = 1700
enemy_freq_max = 7000
last_enemy = pygame.time.get_ticks() - random.randint(enemy_freq_min, enemy_freq_max)

# score code
score = 0
passed_enemy = False
font = pygame.font.SysFont('Bauhaus 93', 90)
white = (255, 255, 255)

def draw_text(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))

# create the player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.run_images = []
        self.jump_images = []
        self.dead_images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            dead_img = pygame.image.load(f'assets/img/player/dead/dead-{num}.png')
            self.dead_images.append(dead_img)
        for num in range(1, 9):
            run_img = pygame.image.load(f'assets/img/player/run/Run-{num}.png')
            jump_img = pygame.image.load(f'assets/img/player/jump/Jump-{num}.png')
            self.run_images.append(run_img)
            self.jump_images.append(jump_img)
            
        self.image = self.run_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel_y = 0
        self.gravity = 8
        self.jump_force = -8
        self.on_ground = True
        self.is_jumping = False
        self.is_dead = False
        self.health = 5 
        self.dead_animation = False

    def update(self, game_over):
        self.counter += 1
        cooldown = 5
        if self.is_dead and not self.dead_animation:
            cooldown = 30  

        if self.counter > cooldown:
            self.counter = 0
            if self.is_jumping:
                self.index += 1
                if self.index >= len(self.jump_images):
                    self.index = 0
                self.image = self.jump_images[self.index]
            elif self.is_dead:
                if not self.dead_animation:
                    self.index += 1
                    if self.index >= len(self.dead_images):
                        self.index = len(self.dead_images) - 1  
                        self.dead_animation = True
                    self.image = self.dead_images[self.index]
            else:
                self.index += 1
                if self.index >= len(self.run_images):
                    self.index = 0
                self.image = self.run_images[self.index]

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.on_ground:
                self.vel_y = self.jump_force
                self.on_ground = False
                self.is_jumping = True

            # gravity physics
            self.vel_y += self.gravity * dt
            self.rect.y += self.vel_y

            # checks if the player hits the ground
            if self.rect.bottom >= 670:
                self.rect.bottom = 670
                self.vel_y = 0
                self.on_ground = True
                self.is_jumping = False

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 9):
            img = pygame.image.load(f'assets/img/player/run/Run-{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.passed = False

    def update(self, game_over):
        if not game_over:
            self.rect.x -= 5
            if self.rect.right < 0:
                self.kill()
            self.counter += 1
            cooldown = 5
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.flip(self.image, True, False)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

class Life(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('assets/img/player/heart2.png')
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image.set_colorkey((255, 255, 255))

def draw_hearts(player_health):
    for i in range(player_health):
        heart = Life(20 + i * 60, 20)  
        life_group.add(heart)

# instantiates from the group class to manage all sprite animations
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()

# instantiate the player class and positions the player sprite
person = Player(175, 630)
player_group.add(person)

run = True
game_over = False

while run:
    dt = clock.tick(fps) / 1000.0

    screen.blit(bg, (-200, -100))

    # draws the floor
    screen.blit(floor, (floor_scroll, 620))
    screen.blit(floor, (floor_scroll + floor_width, 620))

    # score functionality
    for enemy in enemy_group:
        if not enemy.passed and person.rect.left > enemy.rect.right:
            score += 1
            enemy.passed = True

    draw_text(str(score), font, white, 600, 10)

    if not game_over:
        # checks if games over
        if pygame.sprite.groupcollide(player_group, enemy_group, False, True):
            person.health -= 1
            hit.play()

        # generate new enemies
        time_now = pygame.time.get_ticks()
        if time_now - last_enemy > random.randint(enemy_freq_min, enemy_freq_max):
            bad_person = Enemy(1280, 630)
            enemy_group.add(bad_person)
            last_enemy = time_now

        # smooth scrolling
        floor_scroll -= scroll_speed * dt

        # reset floor position if it goes beyond the screen width
        if floor_scroll <= -floor_width:
            floor_scroll = 0

    player_group.update(game_over)
    enemy_group.update(game_over)

    player_group.draw(screen)
    enemy_group.draw(screen)
    life_group.draw(screen)

    for player in player_group:
        player.draw_hitbox(screen)
    for enemy in enemy_group:
        enemy.draw_hitbox(screen)

    # Update the hearts display
    life_group.empty() 
    draw_hearts(person.health)  
    if person.health == 0:
        game_over = True
        person.is_dead = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.mixer.music.stop()
pygame.quit()
