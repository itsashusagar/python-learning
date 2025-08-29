"""
Complete Snake Game using Pygame
A classic implementation with all features in a single file.
"""
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
FPS = 10

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Grid calculations
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE


class Snake:
    def __init__(self, start_position=(10, 10)):
        """Initialize the snake with a starting position."""
        self.body = [start_position]
        self.direction = RIGHT
        self.grow_pending = 0
        
    def move(self):
        """Move the snake one step in the current direction."""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        self.body.insert(0, new_head)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    
    def change_direction(self, new_direction):
        """Change snake direction if it's not opposite to current direction."""
        opposite_directions = {
            UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction
    
    def grow(self):
        """Make the snake grow by one segment on next move."""
        self.grow_pending += 1
    
    def check_collision(self):
        """Check if snake has collided with walls or itself."""
        head = self.body[0]
        head_x, head_y = head
        
        # Check wall collision
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True
            
        # Check self collision
        if head in self.body[1:]:
            return True
            
        return False
    
    def get_head_position(self):
        """Get the position of the snake's head."""
        return self.body[0]
    
    def reset(self, start_position=(10, 10)):
        """Reset the snake to initial state."""
        self.body = [start_position]
        self.direction = RIGHT
        self.grow_pending = 0
    
    def draw(self, screen):
        """Draw the snake on the screen."""
        for i, segment in enumerate(self.body):
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


class Food:
    def __init__(self):
        """Initialize food with a random position."""
        self.position = (5, 5)
        
    def spawn(self, snake_body):
        """Spawn food at a random valid position."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            position = (x, y)
            if position not in snake_body:
                self.position = position
                break
    
    def get_position(self):
        """Get the current food position."""
        return self.position
    
    def draw(self, screen):
        """Draw the food on the screen."""
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)


class SnakeGame:
    def __init__(self):
        """Initialize the game."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.clock = pygame.time.Clock()
        
        # Initialize food position
        self.food.spawn(self.snake.body)
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(RIGHT)
                        
        return True
    
    def update(self):
        """Update game state."""
        if self.game_over:
            return
            
        self.snake.move()
        
        # Check for food consumption
        if self.snake.get_head_position() == self.food.get_position():
            self.snake.grow()
            self.score += 10
            self.food.spawn(self.snake.body)
        
        # Check for collisions
        if self.snake.check_collision():
            self.game_over = True
    
    def draw_grid(self):
        """Draw a subtle grid for visual reference."""
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
    
    def draw(self):
        """Draw all game elements."""
        self.screen.fill(BLACK)
        
        # Draw subtle grid
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (20, 20, 20), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (20, 20, 20), (0, y), (WINDOW_WIDTH, y))
        
        if not self.game_over:
            # Draw game elements
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            
            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            # Draw controls hint
            controls_text = self.small_font.render("Use Arrow Keys or WASD to move", True, GRAY)
            self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))
            
        else:
            self.draw_game_over_screen()
    
    def draw_game_over_screen(self):
        """Draw the game over screen with score and instructions."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over title
        game_over_text = self.title_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        # High score message
        if self.score >= 100:
            high_score_text = self.font.render("Excellent Score!", True, GREEN)
        elif self.score >= 50:
            high_score_text = self.font.render("Good Job!", True, WHITE)
        else:
            high_score_text = self.font.render("Keep Practicing!", True, WHITE)
        
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Instructions
        restart_text = self.font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)
        
        quit_text = self.font.render("Press ESC to quit", True, GRAY)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 110))
        self.screen.blit(quit_text, quit_rect)
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.snake.reset()
        self.food.spawn(self.snake.body)
        self.score = 0
        self.game_over = False
    
    def run(self):
        """Main game loop."""
        print("🐍 Snake Game Started!")
        print("Controls:")
        print("- Arrow Keys or WASD to move")
        print("- SPACE to restart when game over")
        print("- ESC to quit")
        print("- Eat red food to grow and score points!")
        
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the Snake game."""
    try:
        game = SnakeGame()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()