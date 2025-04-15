import pygame
import sys
import random

WIDTH, HEIGHT = 800, 800
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

player_pos = [400, 400]
PLAYER_RADIUS = 25
player_gravity = 0
player_jump = 7

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key =  pygame.key.get_pressed()
    if key[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
        player_gravity = -player_jump


    player_gravity += 0.8
    player_pos[1] += player_gravity
    
    screen.fill(BLACK)
    pygame.draw.circle(screen, GREEN, (int(player_pos[0]), int(player_pos[1])), PLAYER_RADIUS)
    pygame.display.flip() 
    
    
    clock.tick(60)
pygame.quit()
