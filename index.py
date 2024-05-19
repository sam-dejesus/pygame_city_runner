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
scroll_speed = 400  # Adjust scroll speed according to the desired pace
bg = pygame.image.load('img/background/a.webp')
floor = pygame.image.load('img/background/road.gif')

# Stretch the floor image to fit the screen width
floor_width = 1280  
floor_height = 100  
floor = pygame.transform.scale(floor, (floor_width, floor_height))

run = True
while run:
    dt = clock.tick(fps) / 1000.0 

    screen.blit(bg, (-200, -100))
    
    
    # Draw the floor
    screen.blit(floor, (floor_scroll, 620))  # Adjusted Y position to fit the floor at the bottom of the screen
    screen.blit(floor, (floor_scroll + floor_width, 620))  # Draw another floor image to create a seamless loop
    
    # Smooth scrolling
    floor_scroll -= scroll_speed * dt
    
    # Reset floor position if it goes beyond the screen width
    if floor_scroll <= -floor_width:
        floor_scroll = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
