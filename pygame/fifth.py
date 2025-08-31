import tkinter as tk
import random
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        # Game window setup
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        
        # Game constants
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.GRID_SIZE = 20
        self.GRID_WIDTH = self.WINDOW_WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.WINDOW_HEIGHT // self.GRID_SIZE
        self.GAME_SPEED = 150  # milliseconds between moves
        
        # Colors
        self.BG_COLOR = "#1a1a2e"
        self.SNAKE_HEAD_COLOR = "#4ade80"
        self.SNAKE_BODY_COLOR = "#22c55e"
        self.FOOD_COLOR = "#ef4444"
        self.BORDER_COLOR = "#374151"
        self.TEXT_COLOR = "#ffffff"
        self.GRID_COLOR = "#16213e"
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Game state
        self.reset_game()
        
        # Bind events
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.focus_set()
        
        # Start game loop
        self.game_loop()
        
    def reset_game(self):
        """Reset game to initial state"""
        # Snake starts in the middle
        start_x = self.GRID_WIDTH // 2
        start_y = self.GRID_HEIGHT // 2
        
        self.snake = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.high_score = getattr(self, 'high_score', 0)
        
    def generate_food(self):
        """Generate food at random position not occupied by snake"""
        while True:
            food_x = random.randint(0, self.GRID_WIDTH - 1)
            food_y = random.randint(0, self.GRID_HEIGHT - 1)
            
            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.keysym.lower()
        
        if self.game_over:
            if key == 'space' or key == 'return':
                self.reset_game()
            return
        
        if not self.game_started:
            if key in ['up', 'down', 'left', 'right', 'w', 'a', 's', 'd']:
                self.game_started = True
        
        # Direction controls
        if key in ['up', 'w'] and self.direction != Direction.DOWN:
            self.next_direction = Direction.UP
        elif key in ['down', 's'] and self.direction != Direction.UP:
            self.next_direction = Direction.DOWN
        elif key in ['left', 'a'] and self.direction != Direction.RIGHT:
            self.next_direction = Direction.LEFT
        elif key in ['right', 'd'] and self.direction != Direction.LEFT:
            self.next_direction = Direction.RIGHT
    
    def update_snake(self):
        """Update snake position and check for collisions"""
        if not self.game_started or self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Get current head position
        head_x, head_y = self.snake[0]
        
        # Calculate new head position
        dx, dy = self.direction.value
        new_head_x = head_x + dx
        new_head_y = head_y + dy
        
        # Check wall collisions
        if (new_head_x < 0 or new_head_x >= self.GRID_WIDTH or
            new_head_y < 0 or new_head_y >= self.GRID_HEIGHT):
            self.game_over = True
            return
        
        # Check self collision
        if (new_head_x, new_head_y) in self.snake:
            self.game_over = True
            return
        
        # Add new head
        new_head = (new_head_x, new_head_y)
        self.snake.insert(0, new_head)
        
        # Check if food was eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            
            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw_grid(self):
        """Draw subtle grid lines"""
        for x in range(0, self.WINDOW_WIDTH, self.GRID_SIZE):
            self.canvas.create_line(
                x, 0, x, self.WINDOW_HEIGHT,
                fill=self.GRID_COLOR,
                width=1
            )
        
        for y in range(0, self.WINDOW_HEIGHT, self.GRID_SIZE):
            self.canvas.create_line(
                0, y, self.WINDOW_WIDTH, y,
                fill=self.GRID_COLOR,
                width=1
            )
    
    def draw_snake(self):
        """Draw the snake with gradient effect"""
        for i, (x, y) in enumerate(self.snake):
            pixel_x = x * self.GRID_SIZE
            pixel_y = y * self.GRID_SIZE
            
            if i == 0:  # Head
                # Draw head with eyes
                self.canvas.create_rectangle(
                    pixel_x + 1, pixel_y + 1,
                    pixel_x + self.GRID_SIZE - 1, pixel_y + self.GRID_SIZE - 1,
                    fill=self.SNAKE_HEAD_COLOR,
                    outline=self.BORDER_COLOR,
                    width=2
                )
                
                # Draw eyes based on direction
                eye_size = 3
                if self.direction == Direction.RIGHT:
                    eye1_x, eye1_y = pixel_x + 12, pixel_y + 6
                    eye2_x, eye2_y = pixel_x + 12, pixel_y + 14
                elif self.direction == Direction.LEFT:
                    eye1_x, eye1_y = pixel_x + 6, pixel_y + 6
                    eye2_x, eye2_y = pixel_x + 6, pixel_y + 14
                elif self.direction == Direction.UP:
                    eye1_x, eye1_y = pixel_x + 6, pixel_y + 6
                    eye2_x, eye2_y = pixel_x + 14, pixel_y + 6
                else:  # DOWN
                    eye1_x, eye1_y = pixel_x + 6, pixel_y + 14
                    eye2_x, eye2_y = pixel_x + 14, pixel_y + 14
                
                # Draw eyes
                self.canvas.create_oval(
                    eye1_x - eye_size, eye1_y - eye_size,
                    eye1_x + eye_size, eye1_y + eye_size,
                    fill="#000000"
                )
                self.canvas.create_oval(
                    eye2_x - eye_size, eye2_y - eye_size,
                    eye2_x + eye_size, eye2_y + eye_size,
                    fill="#000000"
                )
            else:  # Body
                # Create gradient effect for body segments
                alpha = max(0.3, 1 - (i * 0.1))
                body_color = self.SNAKE_BODY_COLOR
                
                self.canvas.create_rectangle(
                    pixel_x + 2, pixel_y + 2,
                    pixel_x + self.GRID_SIZE - 2, pixel_y + self.GRID_SIZE - 2,
                    fill=body_color,
                    outline=self.BORDER_COLOR,
                    width=1
                )
    
    def draw_food(self):
        """Draw the food with pulsing animation"""
        x, y = self.food
        pixel_x = x * self.GRID_SIZE
        pixel_y = y * self.GRID_SIZE
        
        # Create pulsing effect
        pulse = abs(((self.score * 2) % 20) - 10) / 10
        size_offset = int(pulse * 3)
        
        # Draw food as a circle
        self.canvas.create_oval(
            pixel_x + 3 - size_offset, pixel_y + 3 - size_offset,
            pixel_x + self.GRID_SIZE - 3 + size_offset, pixel_y + self.GRID_SIZE - 3 + size_offset,
            fill=self.FOOD_COLOR,
            outline="#dc2626",
            width=2
        )
        
        # Add shine effect
        self.canvas.create_oval(
            pixel_x + 6, pixel_y + 6,
            pixel_x + 10, pixel_y + 10,
            fill="#fca5a5",
            outline=""
        )
    
    def draw_score(self):
        """Draw score and high score"""
        # Current score
        self.canvas.create_text(
            20, 20,
            text=f"Score: {self.score}",
            font=("Courier", 16, "bold"),
            fill=self.TEXT_COLOR,
            anchor="nw"
        )
        
        # High score
        self.canvas.create_text(
            20, 45,
            text=f"High Score: {self.high_score}",
            font=("Courier", 12),
            fill="#94a3b8",
            anchor="nw"
        )
        
        # Snake length
        self.canvas.create_text(
            self.WINDOW_WIDTH - 20, 20,
            text=f"Length: {len(self.snake)}",
            font=("Courier", 12),
            fill="#94a3b8",
            anchor="ne"
        )
    
    def draw_instructions(self):
        """Draw game instructions"""
        if not self.game_started:
            # Title
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 80,
                text="SNAKE GAME",
                font=("Courier", 36, "bold"),
                fill=self.SNAKE_HEAD_COLOR,
                anchor="center"
            )
            
            # Instructions
            instructions = [
                "Use ARROW KEYS or WASD to move",
                "Eat the red food to grow",
                "Don't hit walls or yourself!",
                "",
                "Press any arrow key to start"
            ]
            
            for i, instruction in enumerate(instructions):
                self.canvas.create_text(
                    self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 20 + (i * 25),
                    text=instruction,
                    font=("Courier", 14),
                    fill=self.TEXT_COLOR,
                    anchor="center"
                )
    
    def draw_game_over(self):
        """Draw game over screen"""
        if self.game_over:
            # Semi-transparent overlay
            self.canvas.create_rectangle(
                0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT,
                fill="#000000",
                stipple="gray50"
            )
            
            # Game over text
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 60,
                text="GAME OVER",
                font=("Courier", 32, "bold"),
                fill="#ef4444",
                anchor="center"
            )
            
            # Final score
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 20,
                text=f"Final Score: {self.score}",
                font=("Courier", 18),
                fill=self.TEXT_COLOR,
                anchor="center"
            )
            
            # Length achieved
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 10,
                text=f"Snake Length: {len(self.snake)}",
                font=("Courier", 14),
                fill="#94a3b8",
                anchor="center"
            )
            
            # High score notification
            if self.score == self.high_score and self.score > 0:
                self.canvas.create_text(
                    self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 40,
                    text="NEW HIGH SCORE!",
                    font=("Courier", 16, "bold"),
                    fill="#fbbf24",
                    anchor="center"
                )
            
            # Restart instruction
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 70,
                text="Press SPACE or ENTER to restart",
                font=("Courier", 12),
                fill=self.TEXT_COLOR,
                anchor="center"
            )
    
    def draw_border(self):
        """Draw decorative border around the game area"""
        border_width = 3
        self.canvas.create_rectangle(
            border_width, border_width,
            self.WINDOW_WIDTH - border_width, self.WINDOW_HEIGHT - border_width,
            fill="",
            outline=self.BORDER_COLOR,
            width=border_width
        )
    
    def draw_everything(self):
        """Draw all game elements"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw background grid
        self.draw_grid()
        
        # Draw border
        self.draw_border()
        
        # Draw game elements
        if self.game_started:
            self.draw_food()
            self.draw_snake()
        
        # Draw UI elements
        self.draw_score()
        
        if not self.game_started:
            self.draw_instructions()
        
        if self.game_over:
            self.draw_game_over()
    
    def draw_grid(self):
        """Draw subtle background grid"""
        for x in range(0, self.WINDOW_WIDTH, self.GRID_SIZE):
            self.canvas.create_line(
                x, 0, x, self.WINDOW_HEIGHT,
                fill=self.GRID_COLOR,
                width=1
            )
        
        for y in range(0, self.WINDOW_HEIGHT, self.GRID_SIZE):
            self.canvas.create_line(
                0, y, self.WINDOW_WIDTH, y,
                fill=self.GRID_COLOR,
                width=1
            )
    
    def update_game(self):
        """Update game state"""
        if not self.game_started or self.game_over:
            return
        
        # Get current head position
        head_x, head_y = self.snake[0]
        
        # Calculate new head position
        dx, dy = self.direction.value
        new_head_x = head_x + dx
        new_head_y = head_y + dy
        
        # Check wall collisions
        if (new_head_x < 0 or new_head_x >= self.GRID_WIDTH or
            new_head_y < 0 or new_head_y >= self.GRID_HEIGHT):
            self.game_over = True
            return
        
        # Check self collision
        if (new_head_x, new_head_y) in self.snake:
            self.game_over = True
            return
        
        # Add new head
        new_head = (new_head_x, new_head_y)
        self.snake.insert(0, new_head)
        
        # Check if food was eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            
            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score
                
            # Increase speed slightly as snake grows
            if len(self.snake) % 5 == 0:
                self.GAME_SPEED = max(80, self.GAME_SPEED - 5)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
        
        # Update direction for next move
        self.direction = self.next_direction
    
    def game_loop(self):
        """Main game loop"""
        self.update_game()
        self.draw_everything()
        
        # Schedule next frame
        self.root.after(self.GAME_SPEED, self.game_loop)
    
    def run(self):
        """Start the game"""
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.WINDOW_WIDTH) // 2
        y = (self.root.winfo_screenheight() - self.WINDOW_HEIGHT) // 2
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()