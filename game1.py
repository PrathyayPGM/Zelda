import pygame
import sys

WIDTH, HEIGHT = 1000, 800
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

player_pos = [400, 400]
PLAYER_RADIUS = 25
player_gravity = 0
player_jump = 20
player_speed = 7
player_facing_right = True  # Track which way player is facing

# Projectile variables
bullet_img = None
bullets = []  # List to store active arrows
bullet_speed = 10
ammo = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load images
try:
    bullet_img = pygame.image.load('bullet.png').convert_alpha()
    bullet_img = pygame.transform.scale(bullet_img, (50, 20))
    bullet_img_left = pygame.transform.flip(bullet_img, True, False)  # Flipped version for left
except:
    print("Couldn't load bullet image, using rectangle instead")
    bullet_img = None

ground = pygame.image.load('ground.png').convert_alpha()
sky = pygame.transform.scale(pygame.image.load('sky2.jpg').convert_alpha(), (WIDTH, HEIGHT))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_pos[1] >= 650:
                player_gravity = -player_jump
            if event.key == pygame.K_SPACE:
                if ammo > 0:
                    bullets.append({
                        'x': player_pos[0],
                        'y': player_pos[1],
                        'rect': pygame.Rect(player_pos[0], player_pos[1], 50, 20),
                        'facing_right': player_facing_right  # Store arrow direction
                    })
                    ammo -= 1
                else:
                    print("No more bullets left as ammo")
    
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player_pos[0] -= player_speed
        player_facing_right = False
    if key[pygame.K_RIGHT]:
        player_pos[0] += player_speed
        player_facing_right = True

    player_gravity += 0.8
    player_pos[1] += player_gravity
    
    # Update arrows
    for bullet in bullets[:]:
        if bullet['facing_right']:
            bullet['x'] += bullet_speed
        else:
            bullet['x'] -= bullet_speed
            
        bullet['rect'].x = bullet['x']
        # Remove arrows that go off screen
        if bullet['x'] > WIDTH or bullet['x'] < 0:
            bullets.remove(arrow)
    
    player_rect = pygame.Rect(
        player_pos[0] - PLAYER_RADIUS,
        player_pos[1] - PLAYER_RADIUS,
        PLAYER_RADIUS * 2,
        PLAYER_RADIUS * 2
    )
    
    player_pos[1] = max(70, min(HEIGHT-70, player_pos[1])) 
    
    screen.fill(BLACK)
    screen.blit(sky, (0, 0))
    
    # Draw arrows
    for bullet in bullets:
        if bullet_img:
            if bullet['facing_right']:
                screen.blit(bullet_img, (bullet['x'], bullet['y']))
            else:
                screen.blit(bullet_img_left, (bullet['x'], bullet['y']))
        else:
            pygame.draw.rect(screen, (255, 0, 0), bullet['rect'])
    
    pygame.draw.circle(screen, GREEN, (int(player_pos[0]), int(player_pos[1])), PLAYER_RADIUS)
    screen.blit(ground, (0, 755))
    pygame.display.flip() 
    
    clock.tick(60)

pygame.quit()
