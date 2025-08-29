import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont(None, 48)

# Game Variables
gravity = 0.5
bird_movement = 0
score = 0
game_active = True

# Bird properties
bird_width = 40
bird_height = 30
bird_x = 100
bird_y = HEIGHT // 2

# Pipe properties
pipe_width = 70
pipe_gap = 200
pipe_speed = 4

# Pipe list
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

# Score tracking for each pipe
passed_pipes = []

# Functions
def draw_bird(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, bird_width, bird_height))

def draw_pipes(pipe_list):
    for pipe in pipe_list:
        pygame.draw.rect(screen, GREEN, pipe)

def create_pipe():
    height = random.randint(150, 450)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

def check_collision(pipe_list):
    global game_active
    for pipe in pipe_list:
        # Collision with top pipe
        if pipe.top == 0 and bird_x + bird_width > pipe.x and bird_x < pipe.x + pipe.width:
            if bird_y < pipe.bottom:
                game_active = False
        # Collision with bottom pipe
        if pipe.bottom == HEIGHT and bird_x + bird_width > pipe.x and bird_x < pipe.x + pipe.width:
            if bird_y + bird_height > pipe.top:
                game_active = False
    # Check screen boundaries
    if bird_y <= 0 or bird_y + bird_height >= HEIGHT:
        game_active = False

def display_score(scr):
    score_display = font.render(f"Score: {int(scr)}", True, BLACK)
    screen.blit(score_display, (10, 10))

# Game Loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = -10
                else:
                    # Reset game
                    game_active = True
                    bird_y = HEIGHT // 2
                    bird_movement = 0
                    pipes.clear()
                    score = 0
                    passed_pipes.clear()

        if event.type == SPAWNPIPE and game_active:
            pipes.extend(create_pipe())

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird_y += bird_movement
        draw_bird(bird_x, bird_y)

        # Move pipes
        for pipe in pipes:
            pipe.x -= pipe_speed
        draw_pipes(pipes)

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x + pipe_width > 0]

        # Check collision
        check_collision(pipes)

        # Score update: increment when bird passes the top pipe
        for pipe in pipes:
            if pipe.top == 0 and pipe not in passed_pipes:
                if bird_x > pipe.x + pipe.width:
                    score += 1
                    passed_pipes.append(pipe)
        display_score(score)

    else:
        # Game Over display
        game_over_display = font.render(f"Game Over! Score: {int(score)}", True, RED)
        screen.blit(game_over_display, (50, HEIGHT//2 - 50))
        restart_display = font.render("Press SPACE to Restart", True, BLACK)
        screen.blit(restart_display, (30, HEIGHT//2 + 10))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
