import pygame
import sys
import random
import time
import math

WIDTH, HEIGHT = 1000, 800
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

player_pos = [400, 400]
PLAYER_RADIUS = 25
player_gravity = 0
player_jump = 20
player_speed = 7
player_facing_right = True
health = 100

# Projectile variables
bullet_img = None
bullets = []
bullet_speed = 10
ammo = 5

pygame.init()
game_state = "menu"
font = pygame.font.SysFont(None, 28)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load images
try:
    bullet_img = pygame.image.load('bullet.png').convert_alpha()
    bullet_img = pygame.transform.scale(bullet_img, (50, 20))
    bullet_img_left = pygame.transform.flip(bullet_img, True, False)
except:
    print("Couldn't load bullet image, using rectangle instead")
    bullet_img = None

# Load player image
try:
    player_img = pygame.image.load('zelda.png').convert_alpha()
    player_img = pygame.transform.scale(player_img, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
    player_img_left = pygame.transform.flip(player_img, True, False)
except:
    print("Couldn't load player image")
    player_img = None

# Load gun image
try:
    gun_img = pygame.image.load('gun.png').convert_alpha()
    gun_img = pygame.transform.scale(gun_img, (40, 20))
    gun_img_left = pygame.transform.flip(gun_img, True, False)
except:
    print("Couldn't load gun image, using rectangle instead")
    gun_img = None

ground = pygame.transform.scale(pygame.image.load('ground.png').convert_alpha(), (WIDTH, HEIGHT // 2))
sky = pygame.transform.scale(pygame.image.load('sky.jpeg').convert_alpha(), (WIDTH, HEIGHT))

def draw_menu():
    screen.fill((20, 20, 20))
    title_font = pygame.font.SysFont(None, 80)
    text_font = pygame.font.SysFont(None, 36)
    
    title = title_font.render("Zelda but GEN ALPHA", True, (0, 255, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    instructions = [
        "left arrow / right arrow - Move",
        "up arrow - Jump",
        "SPACE - Shoot (uses ammo)",
        "Z - Reload",
        "P - Pause",
        "",
        "Click START to begin"
    ]
    for i, line in enumerate(instructions):
        txt = text_font.render(line, True, (255, 255, 255))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 220 + i * 40))

    button_rect = pygame.Rect(WIDTH // 2 - 100, 600, 200, 60)
    pygame.draw.rect(screen, (0, 255, 0), button_rect)
    btn_text = text_font.render("START", True, (0, 0, 0))
    screen.blit(btn_text, (button_rect.centerx - btn_text.get_width() // 2,
                           button_rect.centery - btn_text.get_height() // 2))
    return button_rect

def draw_gun():
    # Calculate gun position based on player position and direction
    if player_facing_right:
        gun_x = player_pos[0] + PLAYER_RADIUS - 5
        gun_y = player_pos[1] - 5
        if gun_img:
            screen.blit(gun_img, (gun_x, gun_y))
        else:
            pygame.draw.rect(screen, (100, 100, 100), (gun_x, gun_y, 40, 10))
    else:
        gun_x = player_pos[0] - PLAYER_RADIUS - 35  # Adjust for flipped position
        gun_y = player_pos[1] - 5
        if gun_img:
            screen.blit(gun_img_left, (gun_x, gun_y))
        else:
            pygame.draw.rect(screen, (100, 100, 100), (gun_x, gun_y, 40, 10))

running = True
while running:
    if game_state == "menu":
        button_rect = draw_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_state = "playing"

    elif game_state == "playing":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_pos[1] >= 650:
                    player_gravity = -player_jump
                if event.key == pygame.K_SPACE:
                    if ammo > 0:
                        # Adjust bullet starting position to come from gun
                        if player_facing_right:
                            bullet_x = player_pos[0] + PLAYER_RADIUS + 30
                        else:
                            bullet_x = player_pos[0] - PLAYER_RADIUS - 30
                        bullets.append({
                            'x': bullet_x,
                            'y': player_pos[1] - 5,  # Align with gun height
                            'rect': pygame.Rect(bullet_x, player_pos[1] - 5, 50, 20),
                            'facing_right': player_facing_right
                        })
                        ammo -= 1
                    else:
                        print("No more bullets left as ammo")
                if event.key == pygame.K_z:
                    time.sleep(0.2)
                    ammo = 5

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player_pos[0] -= player_speed
            player_facing_right = False
        if key[pygame.K_RIGHT]:
            player_pos[0] += player_speed
            player_facing_right = True

        player_gravity += 0.8
        player_pos[1] += player_gravity

        for bullet in bullets[:]:
            if bullet['facing_right']:
                bullet['x'] += bullet_speed
            else:
                bullet['x'] -= bullet_speed

            bullet['rect'].x = bullet['x']
            if bullet['x'] > WIDTH or bullet['x'] < 0:
                bullets.remove(bullet)

        player_rect = pygame.Rect(
            player_pos[0] - PLAYER_RADIUS,
            player_pos[1] - PLAYER_RADIUS,
            PLAYER_RADIUS * 2,
            PLAYER_RADIUS * 2
        )

        player_pos[1] = max(70, min(HEIGHT - 70, player_pos[1]))

        screen.fill(BLACK)
        screen.blit(sky, (0, 0))

        for bullet in bullets:
            if bullet_img:
                if bullet['facing_right']:
                    screen.blit(bullet_img, (bullet['x'], bullet['y']))
                else:
                    screen.blit(bullet_img_left, (bullet['x'], bullet['y']))
            else:
                pygame.draw.rect(screen, (255, 0, 0), bullet['rect'])

        for i in range(ammo):
            pygame.draw.rect(screen, (255, 255, 0), (20 + i * 15, 20, 10, 20))

        pygame.draw.rect(screen, (255, 0, 0), (20, 50, health * 2, 20))
        ammo_label = font.render("Ammo", True, (255, 255, 255))
        screen.blit(ammo_label, (20, 0))
        health_label = font.render("Health", True, (255, 255, 255))
        screen.blit(health_label, (20, 75))

        if player_img:
            img_to_draw = player_img if player_facing_right else player_img_left
            screen.blit(img_to_draw, (player_pos[0] - PLAYER_RADIUS, player_pos[1] - PLAYER_RADIUS))
        else:
            pygame.draw.circle(screen, GREEN, (int(player_pos[0]), int(player_pos[1])), PLAYER_RADIUS)
        
        # Draw the gun after the player so it appears in front
        draw_gun()

        screen.blit(ground, (0, 755))
        pygame.display.flip()

        clock.tick(70)

pygame.quit()
