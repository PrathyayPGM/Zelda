import pygame
import sys
import random
import time
import math
from enum import Enum

# Constants
WIDTH, HEIGHT = 1000, 800
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 70

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3

class Goat:
    def __init__(self):
        self.goat_pos = [1000, 710]
        self.goat_health = 50
        self.goat_speed = 5
        self.attack = 25
        self.goat_radius = 40
        self.load_img()

    def load_img(self):
        try:
            self.image = pygame.image.load('goat.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.goat_radius * 2, self.goat_radius * 2))
            self.image_left = pygame.transform.flip(self.image, True, False)
        except:
            print("Couldn't load goat image, using circle instead")
            self.image = None


class Player:
    def __init__(self):
        self.gun_visible = False
        self.pos = [400, 400]
        self.radius = 40
        self.gravity = 0
        self.jump_power = 20
        self.speed = 7
        self.facing_right = True
        self.health = 100
        self.max_health = 100
        self.ammo = 5
        self.max_ammo = 5
        self.shoot_cooldown = 0
        self.load_images()
        
    def load_images(self):
        try:
            self.image = pygame.image.load('zelda.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
            self.image_left = pygame.transform.flip(self.image, True, False)
        except:
            print("Couldn't load player image, using circle instead")
            self.image = None
            
    def update(self, keys):
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.pos[0] -= self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.pos[0] += self.speed
            self.facing_right = True
            
        # Apply gravity
        self.gravity += 0.8
        self.pos[1] += self.gravity
        
        # Keep player in bounds
        self.pos[1] = max(self.radius, min(HEIGHT - 85, self.pos[1]))
        
        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
    def jump(self):
        if self.pos[1] >= HEIGHT - 85 - self.radius:
            self.gravity = -self.jump_power
            
    def shoot(self):
        if not self.gun_visible:
            print("Can't shoot - gun is hidden!")
            return None
        if self.ammo > 0 and self.shoot_cooldown <= 0:
            self.ammo -= 1
            self.shoot_cooldown = 10  # Cooldown frames
            bullet_x = self.pos[0] + (self.radius + 30 if self.facing_right else -self.radius - 30)
            return {
                'x': bullet_x,
                'y': self.pos[1] - 5,
                'rect': pygame.Rect(bullet_x, self.pos[1] - 5, 50, 20),
                'facing_right': self.facing_right
            }
        return None
        
    def reload(self):
        self.ammo = self.max_ammo
        
    def draw(self, screen):
        if self.image:
            img = self.image if self.facing_right else self.image_left
            screen.blit(img, (self.pos[0] - self.radius, self.pos[1] - self.radius))
        else:
            pygame.draw.circle(screen, GREEN, (int(self.pos[0]), int(self.pos[1])), self.radius)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.goat = Goat()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.player = Player()
        self.bullets = []
        self.load_assets()
        self.setup_audio()

    def update_goat(self):
        if self.goat.goat_health <= 0:  # Don't move if dead
            return
        # Simple movement towards the player
        self.goat.goat_pos[0] -= self.goat.goat_speed 

    def draw_goat(self):
        if self.goat.goat_health <= 0:
            return
        
        if self.goat.image:
            # Determine if goat should face left or right based on player position
            facing_right = self.goat.goat_pos[0] < self.player.pos[0]
            img = self.goat.image if facing_right else self.goat.image_left
            self.screen.blit(img, (self.goat.goat_pos[0] - self.goat.goat_radius, 
                                self.goat.goat_pos[1] - self.goat.goat_radius))
        else:
            pygame.draw.circle(self.screen, (255, 255, 255), 
                            (int(self.goat.goat_pos[0]), int(self.goat.goat_pos[1])), 
                            self.goat.goat_radius) 

    def check_collisions(self):
        # Calculate distance between player and goat
        if self.goat.goat_health <= 0:  # Skip if goat is dead
            return
        dx = self.player.pos[0] - self.goat.goat_pos[0]
        dy = self.player.pos[1] - self.goat.goat_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        # If collision occurs
        if distance < self.player.radius + self.goat.goat_radius:
            self.player.health -= 1  # Or whatever
            
    def load_assets(self):
        # Load bullet image
        try:
            self.bullet_img = pygame.image.load('bullet.png').convert_alpha()
            self.bullet_img = pygame.transform.scale(self.bullet_img, (50, 20))
            self.bullet_img_left = pygame.transform.flip(self.bullet_img, True, False)
        except:
            print("Couldn't load bullet image")
            self.bullet_img = None
            
        # Load gun image
        try:
            self.gun_img = pygame.image.load('gun.png').convert_alpha()
            self.gun_img = pygame.transform.scale(self.gun_img, (100, 60))
            self.gun_img_left = pygame.transform.flip(self.gun_img, True, False)
        except:
            print("Couldn't load gun image")
            self.gun_img = None
            
        # Load background
        try:
            self.ground = pygame.transform.scale(pygame.image.load('ground.png').convert_alpha(), (WIDTH, HEIGHT // 2))
            self.sky = pygame.transform.scale(pygame.image.load('sky.jpeg').convert_alpha(), (WIDTH, HEIGHT))
        except:
            print("Couldn't load background images")
            self.ground = None
            self.sky = None
            
    def setup_audio(self):
        try:
            pygame.mixer.music.load("Game.mp3.mp3")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
            self.gun_toggle_sound = pygame.mixer.Sound("reload.mp3")  
            self.gun_toggle_sound.set_volume(1.0)
        except:
            print("Couldn't load audio files")
            self.gun_toggle_sound = None
            
    def draw_menu(self):
        self.screen.fill((20, 20, 20))
        title_font = pygame.font.SysFont(None, 80)
        text_font = pygame.font.SysFont(None, 36)
        
        title = title_font.render("Zelda but GEN ALPHA", True, (0, 255, 0))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        instructions = [
            "left arrow / right arrow - Move",
            "up arrow - Jump",
            "X - Take gun out", 
            "SPACE - Shoot (uses ammo)",
            "Z - Reload",
            "P - Pause",
            "",
            "Click START to begin"
        ]
        for i, line in enumerate(instructions):
            txt = text_font.render(line, True, WHITE)
            self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 220 + i * 40))

        button_rect = pygame.Rect(WIDTH // 2 - 100, 600, 200, 60)
        pygame.draw.rect(self.screen, (0, 255, 0), button_rect)
        btn_text = text_font.render("START", True, BLACK)
        self.screen.blit(btn_text, (button_rect.centerx - btn_text.get_width() // 2,
                               button_rect.centery - btn_text.get_height() // 2))
        return button_rect
        
    def draw_gun(self):
        if self.player.gun_visible:
            if self.player.facing_right:
                gun_x = self.player.pos[0] + self.player.radius - 38
                gun_y = self.player.pos[1] - 30
                if self.gun_img:
                    self.screen.blit(self.gun_img, (gun_x, gun_y))
            else:
                gun_x = self.player.pos[0] - self.player.radius - 62
                gun_y = self.player.pos[1] - 30
                if self.gun_img:
                    self.screen.blit(self.gun_img_left, (gun_x, gun_y))
                
    def draw_hud(self):
        font = pygame.font.SysFont(None, 28)
        
        # Draw ammo
        for i in range(self.player.ammo):
            pygame.draw.rect(self.screen, (255, 255, 0), (20 + i * 15, 20, 10, 20))
        ammo_label = font.render("Ammo", True, WHITE)
        self.screen.blit(ammo_label, (20, 0))
        gun_status = "READY" if self.player.gun_visible else "HIDDEN"
        status_color = (0, 255, 0) if self.player.gun_visible else (255, 0, 0)
        status_text = font.render(f"Gun: {gun_status}", True, status_color)
        self.screen.blit(status_text, (20, 120))
            
        # Draw health bar
        health_width = (self.player.health / self.player.max_health) * 200
        pygame.draw.rect(self.screen, (255, 0, 0), (20, 50, health_width, 20))
        health_label = font.render("Health", True, WHITE)
        self.screen.blit(health_label, (20, 75))
        
    def update_bullets(self):
        for bullet in self.bullets[:]:
            if bullet['facing_right']:
                bullet['x'] += 25
            else:
                bullet['x'] -= 25

            bullet['rect'].x = bullet['x'] 
            if bullet['x'] > WIDTH or bullet['x'] < 0:
                self.bullets.remove(bullet)
        
            dx = bullet['x'] - self.goat.goat_pos[0]
            dy = bullet['y'] - self.goat.goat_pos[1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < self.goat.goat_radius:
                self.goat.goat_health -= 25
                self.bullets.remove(bullet)
                continue
                
    def draw_bullets(self):
        for bullet in self.bullets:
            if self.bullet_img:
                img = self.bullet_img if bullet['facing_right'] else self.bullet_img_left
                self.screen.blit(img, (bullet['x'], bullet['y']))
            else:
                pygame.draw.rect(self.screen, (255, 0, 0), bullet['rect'])
                
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.state == GameState.MENU:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        button_rect = self.draw_menu()
                        if button_rect.collidepoint(event.pos):
                            self.state = GameState.PLAYING
                            
                elif self.state == GameState.PLAYING:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:  
                            self.player.gun_visible = not self.player.gun_visible
                            if hasattr(self, 'gun_toggle_sound') and self.gun_toggle_sound:
                                self.gun_toggle_sound.play()
                        if event.key == pygame.K_UP:
                            self.player.jump()
                        if event.key == pygame.K_SPACE:
                            bullet = self.player.shoot()
                            if bullet:
                                self.bullets.append(bullet)
                        if event.key == pygame.K_z:
                            self.player.reload()
                        if event.key == pygame.K_p:
                            self.state = GameState.PAUSED
                            
                elif self.state == GameState.PAUSED:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                        
            if self.state == GameState.MENU:
                self.draw_menu()
                
            elif self.state == GameState.PLAYING:
                keys = pygame.key.get_pressed()
                self.player.update(keys)
                self.update_bullets()
                self.update_goat()
                self.check_collisions()
                
                # Draw everything
                if self.sky:
                    self.screen.blit(self.sky, (0, 0))
                else:
                    self.screen.fill(BLACK)
                    
                self.draw_bullets()
                self.player.draw(self.screen)
                self.draw_gun()
                self.draw_hud()
                self.draw_goat()
                
                if self.ground:
                    self.screen.blit(self.ground, (0, 755))
                    
                if self.player.health <= 0:
                    self.state = GameState.GAME_OVER
                    
            elif self.state == GameState.GAME_OVER:
                font = pygame.font.SysFont(None, 72)
                text = font.render("GAME OVER", True, (0, 255, 255))
                self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
                pygame.display.flip()
                time.sleep(2)
                running = False
                
            elif self.state == GameState.PAUSED:
                font = pygame.font.SysFont(None, 72)
                text = font.render("PAUSED", True, WHITE)
                self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
