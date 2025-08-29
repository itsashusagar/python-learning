# Simple Catch the Falling Object Game using Pygame

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Object")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Player properties
player_width = 100
player_height = 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 10

# Object properties
object_width = 50
object_height = 50
object_x = random.randint(0, WIDTH - object_width)
object_y = -50
object_speed = 5

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game Loop
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Update object position
    object_y += object_speed

    # Check for collision
    if (object_y + object_height >= player_y) and (player_x < object_x + object_width) and (player_x + player_width > object_x):
        score += 1
        object_x = random.randint(0, WIDTH - object_width)
        object_y = -50

    # Reset object if it goes off screen
    if object_y > HEIGHT:
        object_x = random.randint(0, WIDTH - object_width)
        object_y = -50

    # Draw player and object
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, RED, (object_x, object_y, object_width, object_height))

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
