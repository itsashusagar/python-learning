import tkinter as tk
import random
import math

class FlappyBird:
    def __init__(self):
        # Game window setup
        self.root = tk.Tk()
        self.root.title("Flappy Bird")
        self.root.resizable(False, False)
        
        # Game constants
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.BIRD_SIZE = 30
        self.PIPE_WIDTH = 80
        self.PIPE_GAP = 200
        self.GRAVITY = 0.5
        self.JUMP_VELOCITY = -10
        self.PIPE_VELOCITY = -3
        self.GROUND_HEIGHT = 100
        
        # Colors
        self.SKY_COLOR = "#87CEEB"
        self.BIRD_COLOR = "#FFD700"
        self.PIPE_COLOR = "#228B22"
        self.GROUND_COLOR = "#8B4513"
        self.WHITE = "#FFFFFF"
        self.BLACK = "#000000"
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT,
            bg=self.SKY_COLOR
        )
        self.canvas.pack()
        
        # Game state
        self.reset_game()
        
        # Bind events
        self.root.bind('<KeyPress-space>', self.jump)
        self.root.bind('<Button-1>', self.jump)  # Mouse click
        self.root.focus_set()
        
        # Start game loop
        self.game_loop()
        
    def reset_game(self):
        """Reset game to initial state"""
        self.bird_x = 100
        self.bird_y = self.WINDOW_HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.game_started = False
        
        # Create initial pipes
        for i in range(3):
            pipe_x = self.WINDOW_WIDTH + i * 300
            pipe_height = random.randint(100, self.WINDOW_HEIGHT - self.PIPE_GAP - self.GROUND_HEIGHT - 100)
            self.pipes.append({
                'x': pipe_x,
                'height': pipe_height,
                'passed': False
            })
    
    def jump(self, event=None):
        """Make bird jump"""
        if self.game_over:
            self.reset_game()
        else:
            self.bird_velocity = self.JUMP_VELOCITY
            if not self.game_started:
                self.game_started = True
    
    def update_bird(self):
        """Update bird position and velocity"""
        if self.game_started and not self.game_over:
            self.bird_velocity += self.GRAVITY
            self.bird_y += self.bird_velocity
            
            # Check ground collision
            if self.bird_y > self.WINDOW_HEIGHT - self.GROUND_HEIGHT - self.BIRD_SIZE // 2:
                self.bird_y = self.WINDOW_HEIGHT - self.GROUND_HEIGHT - self.BIRD_SIZE // 2
                self.game_over = True
            
            # Check ceiling collision
            if self.bird_y < self.BIRD_SIZE // 2:
                self.bird_y = self.BIRD_SIZE // 2
                self.bird_velocity = 0
    
    def update_pipes(self):
        """Update pipe positions and create new pipes"""
        if not self.game_started or self.game_over:
            return
            
        for pipe in self.pipes:
            pipe['x'] += self.PIPE_VELOCITY
            
            # Check if bird passed the pipe for scoring
            if not pipe['passed'] and pipe['x'] + self.PIPE_WIDTH < self.bird_x:
                pipe['passed'] = True
                self.score += 1
        
        # Remove pipes that have moved off screen
        self.pipes = [pipe for pipe in self.pipes if pipe['x'] > -self.PIPE_WIDTH]
        
        # Add new pipes when needed
        if len(self.pipes) < 3:
            last_pipe_x = max(pipe['x'] for pipe in self.pipes) if self.pipes else self.WINDOW_WIDTH
            if last_pipe_x < self.WINDOW_WIDTH + 100:
                pipe_height = random.randint(100, self.WINDOW_HEIGHT - self.PIPE_GAP - self.GROUND_HEIGHT - 100)
                self.pipes.append({
                    'x': last_pipe_x + 300,
                    'height': pipe_height,
                    'passed': False
                })
    
    def check_collisions(self):
        """Check for collisions between bird and pipes"""
        if not self.game_started or self.game_over:
            return
            
        bird_left = self.bird_x - self.BIRD_SIZE // 2
        bird_right = self.bird_x + self.BIRD_SIZE // 2
        bird_top = self.bird_y - self.BIRD_SIZE // 2
        bird_bottom = self.bird_y + self.BIRD_SIZE // 2
        
        for pipe in self.pipes:
            pipe_left = pipe['x']
            pipe_right = pipe['x'] + self.PIPE_WIDTH
            
            # Check if bird is horizontally aligned with pipe
            if bird_right > pipe_left and bird_left < pipe_right:
                # Check collision with top pipe
                if bird_top < pipe['height']:
                    self.game_over = True
                    return
                
                # Check collision with bottom pipe
                bottom_pipe_top = pipe['height'] + self.PIPE_GAP
                if bird_bottom > bottom_pipe_top:
                    self.game_over = True
                    return
    
    def draw_bird(self):
        """Draw the bird with simple animation"""
        # Calculate rotation based on velocity
        rotation = max(-30, min(30, self.bird_velocity * 3))
        
        # Draw bird body (circle)
        self.canvas.create_oval(
            self.bird_x - self.BIRD_SIZE // 2,
            self.bird_y - self.BIRD_SIZE // 2,
            self.bird_x + self.BIRD_SIZE // 2,
            self.bird_y + self.BIRD_SIZE // 2,
            fill=self.BIRD_COLOR,
            outline=self.BLACK,
            width=2
        )
        
        # Draw bird eye
        eye_x = self.bird_x + 5
        eye_y = self.bird_y - 5
        self.canvas.create_oval(
            eye_x - 3, eye_y - 3,
            eye_x + 3, eye_y + 3,
            fill=self.WHITE,
            outline=self.BLACK
        )
        
        # Draw pupil
        self.canvas.create_oval(
            eye_x - 1, eye_y - 1,
            eye_x + 1, eye_y + 1,
            fill=self.BLACK
        )
        
        # Draw beak
        beak_points = [
            self.bird_x + self.BIRD_SIZE // 2, self.bird_y,
            self.bird_x + self.BIRD_SIZE // 2 + 10, self.bird_y - 3,
            self.bird_x + self.BIRD_SIZE // 2 + 10, self.bird_y + 3
        ]
        self.canvas.create_polygon(beak_points, fill="#FFA500", outline=self.BLACK)
    
    def draw_pipes(self):
        """Draw all pipes"""
        for pipe in self.pipes:
            # Top pipe
            self.canvas.create_rectangle(
                pipe['x'], 0,
                pipe['x'] + self.PIPE_WIDTH, pipe['height'],
                fill=self.PIPE_COLOR,
                outline=self.BLACK,
                width=2
            )
            
            # Bottom pipe
            bottom_pipe_top = pipe['height'] + self.PIPE_GAP
            self.canvas.create_rectangle(
                pipe['x'], bottom_pipe_top,
                pipe['x'] + self.PIPE_WIDTH, self.WINDOW_HEIGHT - self.GROUND_HEIGHT,
                fill=self.PIPE_COLOR,
                outline=self.BLACK,
                width=2
            )
            
            # Pipe caps
            cap_height = 30
            cap_width = self.PIPE_WIDTH + 10
            
            # Top pipe cap
            self.canvas.create_rectangle(
                pipe['x'] - 5, pipe['height'] - cap_height,
                pipe['x'] + cap_width - 5, pipe['height'],
                fill=self.PIPE_COLOR,
                outline=self.BLACK,
                width=2
            )
            
            # Bottom pipe cap
            self.canvas.create_rectangle(
                pipe['x'] - 5, bottom_pipe_top,
                pipe['x'] + cap_width - 5, bottom_pipe_top + cap_height,
                fill=self.PIPE_COLOR,
                outline=self.BLACK,
                width=2
            )
    
    def draw_ground(self):
        """Draw the ground"""
        ground_y = self.WINDOW_HEIGHT - self.GROUND_HEIGHT
        self.canvas.create_rectangle(
            0, ground_y,
            self.WINDOW_WIDTH, self.WINDOW_HEIGHT,
            fill=self.GROUND_COLOR,
            outline=self.BLACK,
            width=2
        )
        
        # Add some grass texture
        for i in range(0, self.WINDOW_WIDTH, 20):
            self.canvas.create_line(
                i, ground_y,
                i + 10, ground_y - 5,
                fill="#90EE90",
                width=2
            )
    
    def draw_clouds(self):
        """Draw background clouds"""
        cloud_positions = [(150, 100), (400, 80), (650, 120), (200, 200), (500, 180)]
        
        for cx, cy in cloud_positions:
            # Animate clouds slightly
            offset = (self.score * 0.5) % 50
            cloud_x = (cx - offset) % (self.WINDOW_WIDTH + 100)
            
            # Draw cloud as multiple overlapping circles
            for dx, dy, size in [(-15, 0, 20), (0, -10, 25), (15, 0, 20), (0, 10, 15)]:
                self.canvas.create_oval(
                    cloud_x + dx - size, cy + dy - size,
                    cloud_x + dx + size, cy + dy + size,
                    fill=self.WHITE,
                    outline=""
                )
    
    def draw_score(self):
        """Draw the current score"""
        self.canvas.create_text(
            self.WINDOW_WIDTH // 2, 50,
            text=f"Score: {self.score}",
            font=("Arial", 24, "bold"),
            fill=self.WHITE,
            anchor="center"
        )
        
        # Add shadow for better visibility
        self.canvas.create_text(
            self.WINDOW_WIDTH // 2 + 2, 52,
            text=f"Score: {self.score}",
            font=("Arial", 24, "bold"),
            fill=self.BLACK,
            anchor="center"
        )
    
    def draw_instructions(self):
        """Draw game instructions"""
        if not self.game_started:
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 100,
                text="FLAPPY BIRD",
                font=("Arial", 32, "bold"),
                fill=self.WHITE,
                anchor="center"
            )
            
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2 + 2, self.WINDOW_HEIGHT // 2 - 98,
                text="FLAPPY BIRD",
                font=("Arial", 32, "bold"),
                fill=self.BLACK,
                anchor="center"
            )
            
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2,
                text="Press SPACEBAR or CLICK to jump!",
                font=("Arial", 16),
                fill=self.WHITE,
                anchor="center"
            )
            
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2 + 1, self.WINDOW_HEIGHT // 2 + 1,
                text="Press SPACEBAR or CLICK to jump!",
                font=("Arial", 16),
                fill=self.BLACK,
                anchor="center"
            )
    
    def draw_game_over(self):
        """Draw game over screen"""
        if self.game_over:
            # Semi-transparent overlay
            self.canvas.create_rectangle(
                0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT,
                fill=self.BLACK,
                stipple="gray25"
            )
            
            # Game over text
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 50,
                text="GAME OVER",
                font=("Arial", 36, "bold"),
                fill="#FF4444",
                anchor="center"
            )
            
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2,
                text=f"Final Score: {self.score}",
                font=("Arial", 20),
                fill=self.WHITE,
                anchor="center"
            )
            
            self.canvas.create_text(
                self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 40,
                text="Press SPACEBAR or CLICK to restart",
                font=("Arial", 16),
                fill=self.WHITE,
                anchor="center"
            )
    
    def draw_everything(self):
        """Draw all game elements"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw background elements
        self.draw_clouds()
        
        # Draw game elements
        self.draw_pipes()
        self.draw_ground()
        self.draw_bird()
        
        # Draw UI elements
        self.draw_score()
        
        if not self.game_started:
            self.draw_instructions()
        
        if self.game_over:
            self.draw_game_over()
    
    def game_loop(self):
        """Main game loop"""
        if self.game_started and not self.game_over:
            self.update_bird()
            self.update_pipes()
            self.check_collisions()
        
        self.draw_everything()
        
        # Schedule next frame
        self.root.after(16, self.game_loop)  # ~60 FPS
    
    def run(self):
        """Start the game"""
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.WINDOW_WIDTH) // 2
        y = (self.root.winfo_screenheight() - self.WINDOW_HEIGHT) // 2
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    game = FlappyBird()
    game.run()