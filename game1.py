import pygame
import sys
import random

WIDTH, HEIGHT = 1000, 800
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

player_pos = [400, 400]
PLAYER_RADIUS = 25
player_gravity = 0
player_jump = 20
player_speed = 7

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
ground = pygame.image.load('ground.png').convert_alpha()
sky = pygame.transform.scale(pygame.image.load('sky2.jpg').convert_alpha(), (WIDTH, HEIGHT))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  # Moved inside event loop
            if event.key == pygame.K_UP and player_pos[1] >= 650:
                player_gravity = -player_jump

    
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if key[pygame.K_RIGHT]:
        player_pos[0] += player_speed



    player_gravity += 0.8
    player_pos[1] += player_gravity
    
    
    player_rect = pygame.Rect(
        player_pos[0] - PLAYER_RADIUS,  # Left edge
        player_pos[1] - PLAYER_RADIUS,  # Top edge
        PLAYER_RADIUS * 2,              # Width
        PLAYER_RADIUS * 2               # Height 
)
    
    player_pos[1] = max(70, min(HEIGHT-70, player_pos[1])) 
    
    screen.fill(BLACK)
    screen.blit(sky, (0, 0))
    pygame.draw.circle(screen, GREEN, (int(player_pos[0]), int(player_pos[1])), PLAYER_RADIUS)
    screen.blit(ground, (0, 755))
    pygame.display.flip() 
    
    
    clock.tick(60)
pygame.quit()
