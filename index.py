# imports pygame lib
import pygame
from pygame.locals import *
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

enemy_freq = 1500
last_enemy = pygame.time.get_ticks() - enemy_freq

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
        self.gravity = 5
        self.jump_force = -5
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



# instantiates from the group class to manage all sprite animations
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
# instantiate the player class and positions the player sprite
# bad_person = Enemy(675, 630)
person = Player(175, 630) 

player_group.add(person)
# enemy_group.add(bad_person)

run = True
game_over = False

while run:
    dt = clock.tick(fps) / 1000.0 

    screen.blit(bg, (-200, -100))
    
    
    # draws the floor
    screen.blit(floor, (floor_scroll, 620)) 
    screen.blit(floor, (floor_scroll + floor_width, 620))  
    
    if game_over == False:
    # generate new enemies
        time_now = pygame.time.get_ticks()
    # checks if games over
        if pygame.sprite.groupcollide(player_group, enemy_group, False, True):
            game_over = True

        if time_now - last_enemy > enemy_freq:
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
