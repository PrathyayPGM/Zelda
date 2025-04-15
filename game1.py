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
arrow_img = None
arrows = []  # List to store active arrows
arrow_speed = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load images
try:
    arrow_img = pygame.image.load('bullet.png').convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (50, 20))
    arrow_img_left = pygame.transform.flip(arrow_img, True, False)  # Flipped version for left
except:
    print("Couldn't load arrow image, using rectangle instead")
    arrow_img = None

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
                # Create a new arrow at player's position with direction
                arrows.append({
                    'x': player_pos[0],
                    'y': player_pos[1],
                    'rect': pygame.Rect(player_pos[0], player_pos[1], 50, 20),
                    'facing_right': player_facing_right  # Store arrow direction
                })
    
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
    for arrow in arrows[:]:
        if arrow['facing_right']:
            arrow['x'] += arrow_speed
        else:
            arrow['x'] -= arrow_speed
            
        arrow['rect'].x = arrow['x']
        # Remove arrows that go off screen
        if arrow['x'] > WIDTH or arrow['x'] < 0:
            arrows.remove(arrow)
    
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
    for arrow in arrows:
        if arrow_img:
            if arrow['facing_right']:
                screen.blit(arrow_img, (arrow['x'], arrow['y']))
            else:
                screen.blit(arrow_img_left, (arrow['x'], arrow['y']))
        else:
            pygame.draw.rect(screen, (255, 0, 0), arrow['rect'])
    
    pygame.draw.circle(screen, GREEN, (int(player_pos[0]), int(player_pos[1])), PLAYER_RADIUS)
    screen.blit(ground, (0, 755))
    pygame.display.flip() 
    
    clock.tick(60)

pygame.quit()
