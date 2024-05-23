# imports pygame lib
import pygame
from pygame.locals import *
import random
pygame.init()

#  used to set the fps speed
clock = pygame.time.Clock()
fps = 60

# screen size
screen = pygame.display.set_mode((1280, 720))

# title of the game when program starts
pygame.display.set_caption('City Runner')
# stores background and floor img in a var as well as sets scroll speed 
floor_scroll = 0
scroll_speed = 400  # Adjust scroll speed
bg = pygame.image.load('img/background/a.webp')
floor = pygame.image.load('img/background/road.gif')

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
    image = font.render(text, True, color, )
    screen.blit(image, (x, y))

# create the player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,9):
            img = pygame.image.load(f'img/player/run//Run-{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel_y = 0
        self.gravity = 8
        self.jump_force = -8
        self.on_ground = True 

    def update(self):
        self.counter += 1
        cooldown = 5
        if self.counter > cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False

        # gravity physics 
        self.vel_y += self.gravity * dt
        self.rect.y += self.vel_y

        # checks if the player hits the ground
        if self.rect.bottom >= 670:  
            self.rect.bottom = 670
            self.vel_y = 0
            self.on_ground = True
    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,9):
            img = pygame.image.load(f'img/player/run//Run-{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.passed = False

    def update(self):
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



# instantiates from the group class to manage all sprite animations
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
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
    
    if game_over == False:
    
    # checks if games over
        if pygame.sprite.groupcollide(player_group, enemy_group, False, True):
            game_over = True

        # generate new enemies
        time_now = pygame.time.get_ticks()
        if time_now - last_enemy > random.randint(enemy_freq_min, enemy_freq_max):  # Step 3: Randomize enemy frequency
            bad_person = Enemy(1280, 630)
            enemy_group.add(bad_person)
            last_enemy = time_now

    
    # smooth scrolling
        floor_scroll -= scroll_speed * dt
    
    # reset floor position if it goes beyond the screen width
        if floor_scroll <= -floor_width:
            floor_scroll = 0

        player_group.draw(screen)
        enemy_group.draw(screen)
        player_group.update()
        enemy_group.update()

    for player in player_group:
            player.draw_hitbox(screen)
    for enemy in enemy_group:
            enemy.draw_hitbox(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
