#!/usr/bin/env python3
"""
Advanced Snake Game
A sophisticated implementation of the classic Snake game with multiple features.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json
import os

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

@dataclass
class Point:
    x: int
    y: int
    
    def __add__(self, other):
        if isinstance(other, Direction):
            return Point(self.x + other.value[0], self.y + other.value[1])
        return Point(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    HIGH_SCORES = "high_scores"

class SnakeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Snake Game")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
        # Game constants
        self.GRID_SIZE = 20
        self.GRID_WIDTH = 30
        self.GRID_HEIGHT = 25
        self.CANVAS_WIDTH = self.GRID_WIDTH * self.GRID_SIZE
        self.CANVAS_HEIGHT = self.GRID_HEIGHT * self.GRID_SIZE
        
        # Game state
        self.state = GameState.MENU
        self.snake = [Point(15, 12), Point(14, 12), Point(13, 12)]
        self.direction = Direction.RIGHT
        self.food = Point(20, 12)
        self.score = 0
        self.level = 1
        self.speed = 150
        self.high_scores = self.load_high_scores()
        self.power_ups = []
        self.special_food = None
        self.invincible_time = 0
        
        # Colors
        self.colors = {
            'bg': '#0f0f0f',
            'snake': '#00ff00',
            'snake_head': '#00cc00',
            'food': '#ff0000',
            'special_food': '#ffd700',
            'power_up': '#ff00ff',
            'grid': '#333333',
            'text': '#ffffff',
            'button': '#4a4a4a',
            'button_hover': '#6a6a6a'
        }
        
        self.setup_ui()
        self.bind_keys()
        
    def setup_ui(self):
        """Initialize the user interface"""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Menu frame
        self.menu_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        
        # Game frame
        self.game_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        
        # Canvas for game
        self.canvas = tk.Canvas(
            self.game_frame,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        
        # Score and info labels
        self.info_frame = tk.Frame(self.game_frame, bg='#1a1a1a')
        self.score_label = tk.Label(
            self.info_frame,
            text="Score: 0",
            font=("Arial", 16, "bold"),
            fg=self.colors['text'],
            bg='#1a1a1a'
        )
        self.level_label = tk.Label(
            self.info_frame,
            text="Level: 1",
            font=("Arial", 16, "bold"),
            fg=self.colors['text'],
            bg='#1a1a1a'
        )
        
        self.setup_menu()
        self.show_menu()
        
    def setup_menu(self):
        """Setup the main menu"""
        title = tk.Label(
            self.menu_frame,
            text="ADVANCED SNAKE",
            font=("Arial", 32, "bold"),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title.pack(pady=50)
        
        subtitle = tk.Label(
            self.menu_frame,
            text="Navigate with WASD or Arrow Keys",
            font=("Arial", 14),
            fg=self.colors['text'],
            bg='#1a1a1a'
        )
        subtitle.pack(pady=10)
        
        # Menu buttons
        button_style = {
            'font': ("Arial", 14, "bold"),
            'fg': self.colors['text'],
            'bg': self.colors['button'],
            'activeforeground': self.colors['text'],
            'activebackground': self.colors['button_hover'],
            'relief': 'flat',
            'bd': 0,
            'pady': 10,
            'padx': 30
        }
        
        start_btn = tk.Button(
            self.menu_frame,
            text="START GAME",
            command=self.start_game,
            **button_style
        )
        start_btn.pack(pady=10)
        
        scores_btn = tk.Button(
            self.menu_frame,
            text="HIGH SCORES",
            command=self.show_high_scores,
            **button_style
        )
        scores_btn.pack(pady=10)
        
        quit_btn = tk.Button(
            self.menu_frame,
            text="QUIT",
            command=self.root.quit,
            **button_style
        )
        quit_btn.pack(pady=10)
        
    def bind_keys(self):
        """Bind keyboard events"""
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
        
    def on_key_press(self, event):
        """Handle keyboard input"""
        if self.state == GameState.PLAYING:
            key = event.keysym.lower()
            
            # Movement keys
            if key in ['w', 'up'] and self.direction != Direction.DOWN:
                self.direction = Direction.UP
            elif key in ['s', 'down'] and self.direction != Direction.UP:
                self.direction = Direction.DOWN
            elif key in ['a', 'left'] and self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
            elif key in ['d', 'right'] and self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
            elif key == 'p':
                self.toggle_pause()
        elif self.state == GameState.PAUSED:
            if event.keysym.lower() == 'p':
                self.toggle_pause()
        elif self.state == GameState.GAME_OVER:
            if event.keysym.lower() == 'r':
                self.start_game()
            elif event.keysym.lower() == 'escape':
                self.show_menu()
                
    def start_game(self):
        """Initialize and start a new game"""
        self.state = GameState.PLAYING
        self.snake = [Point(15, 12), Point(14, 12), Point(13, 12)]
        self.direction = Direction.RIGHT
        self.score = 0
        self.level = 1
        self.speed = 150
        self.power_ups = []
        self.special_food = None
        self.invincible_time = 0
        
        self.place_food()
        self.show_game()
        self.game_loop()
        
    def show_menu(self):
        """Display the main menu"""
        self.state = GameState.MENU
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        
    def show_game(self):
        """Display the game screen"""
        self.menu_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Pack game elements
        self.info_frame.pack(pady=10)
        self.score_label.pack(side=tk.LEFT, padx=20)
        self.level_label.pack(side=tk.LEFT, padx=20)
        self.canvas.pack(pady=10)
        
    def show_high_scores(self):
        """Display high scores window"""
        scores_window = tk.Toplevel(self.root)
        scores_window.title("High Scores")
        scores_window.geometry("300x400")
        scores_window.configure(bg='#1a1a1a')
        scores_window.resizable(False, False)
        
        title = tk.Label(
            scores_window,
            text="HIGH SCORES",
            font=("Arial", 20, "bold"),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title.pack(pady=20)
        
        for i, score in enumerate(self.high_scores[:10], 1):
            score_text = f"{i:2d}. {score:6d}"
            score_label = tk.Label(
                scores_window,
                text=score_text,
                font=("Courier", 14),
                fg=self.colors['text'],
                bg='#1a1a1a'
            )
            score_label.pack(pady=2)
            
    def place_food(self):
        """Place food at a random location"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            food_pos = Point(x, y)
            
            if food_pos not in self.snake:
                self.food = food_pos
                break
                
        # Chance for special food
        if random.random() < 0.1:  # 10% chance
            self.place_special_food()
            
        # Chance for power-up
        if random.random() < 0.05 and len(self.power_ups) < 2:  # 5% chance
            self.place_power_up()
            
    def place_special_food(self):
        """Place special food that gives bonus points"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            pos = Point(x, y)
            
            if pos not in self.snake and pos != self.food:
                self.special_food = pos
                # Special food disappears after 5 seconds
                self.root.after(5000, self.remove_special_food)
                break
                
    def place_power_up(self):
        """Place a power-up on the grid"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            pos = Point(x, y)
            
            if (pos not in self.snake and pos != self.food and 
                pos != self.special_food and pos not in self.power_ups):
                self.power_ups.append(pos)
                # Power-up disappears after 8 seconds
                self.root.after(8000, lambda p=pos: self.remove_power_up(p))
                break
                
    def remove_special_food(self):
        """Remove special food from the grid"""
        self.special_food = None
        
    def remove_power_up(self, power_up_pos):
        """Remove a specific power-up from the grid"""
        if power_up_pos in self.power_ups:
            self.power_ups.remove(power_up_pos)
            
    def move_snake(self):
        """Move the snake and handle collisions"""
        if self.state != GameState.PLAYING:
            return
            
        # Calculate new head position
        head = self.snake[0]
        new_head = head + self.direction
        
        # Handle wall collision (wrap around)
        new_head.x = new_head.x % self.GRID_WIDTH
        new_head.y = new_head.y % self.GRID_HEIGHT
        
        # Check self collision (unless invincible)
        if self.invincible_time <= 0 and new_head in self.snake:
            self.game_over()
            return
            
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check food collision
        ate_food = False
        if new_head == self.food:
            self.score += 10 * self.level
            ate_food = True
            self.place_food()
            
        # Check special food collision
        elif self.special_food and new_head == self.special_food:
            self.score += 50 * self.level
            ate_food = True
            self.special_food = None
            
        # Check power-up collision
        elif new_head in self.power_ups:
            self.power_ups.remove(new_head)
            self.activate_power_up()
            
        # Remove tail if no food eaten
        if not ate_food:
            self.snake.pop()
        else:
            # Check for level up
            if self.score >= self.level * 200:
                self.level_up()
                
        # Decrease invincibility time
        if self.invincible_time > 0:
            self.invincible_time -= 1
            
    def activate_power_up(self):
        """Activate a random power-up effect"""
        effects = ['invincible', 'slow_time', 'bonus_points', 'shrink']
        effect = random.choice(effects)
        
        if effect == 'invincible':
            self.invincible_time = 30  # 30 moves of invincibility
        elif effect == 'slow_time':
            self.speed = min(self.speed + 50, 300)  # Temporarily slow down
            self.root.after(3000, self.restore_speed)
        elif effect == 'bonus_points':
            self.score += 100 * self.level
        elif effect == 'shrink':
            if len(self.snake) > 3:
                self.snake = self.snake[:len(self.snake)//2]
                
    def restore_speed(self):
        """Restore normal game speed"""
        self.speed = max(50, 150 - (self.level - 1) * 10)
        
    def level_up(self):
        """Increase game level and difficulty"""
        self.level += 1
        self.speed = max(50, self.speed - 10)  # Increase speed
        
        # Show level up message
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2,
            self.CANVAS_HEIGHT // 2,
            text=f"LEVEL {self.level}!",
            font=("Arial", 24, "bold"),
            fill='#ffff00',
            tags="level_up"
        )
        self.root.after(1500, lambda: self.canvas.delete("level_up"))
        
    def toggle_pause(self):
        """Toggle game pause state"""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            self.game_loop()
            
    def game_over(self):
        """Handle game over"""
        self.state = GameState.GAME_OVER
        self.update_high_scores()
        
        # Show game over screen
        self.canvas.create_rectangle(
            0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT,
            fill='#000000', stipple='gray50', tags="game_over"
        )
        
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2,
            self.CANVAS_HEIGHT // 2 - 60,
            text="GAME OVER",
            font=("Arial", 32, "bold"),
            fill='#ff0000',
            tags="game_over"
        )
        
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2,
            self.CANVAS_HEIGHT // 2 - 20,
            text=f"Final Score: {self.score}",
            font=("Arial", 18, "bold"),
            fill=self.colors['text'],
            tags="game_over"
        )
        
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2,
            self.CANVAS_HEIGHT // 2 + 20,
            text=f"Level Reached: {self.level}",
            font=("Arial", 16),
            fill=self.colors['text'],
            tags="game_over"
        )
        
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2,
            self.CANVAS_HEIGHT // 2 + 60,
            text="Press 'R' to restart or 'ESC' for menu",
            font=("Arial", 14),
            fill='#cccccc',
            tags="game_over"
        )
        
    def update_high_scores(self):
        """Update high scores with current score"""
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10
        self.save_high_scores()
        
    def load_high_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists('high_scores.json'):
                with open('high_scores.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return [0] * 10
        
    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open('high_scores.json', 'w') as f:
                json.dump(self.high_scores, f)
        except:
            pass
            
    def draw_grid(self):
        """Draw background grid"""
        self.canvas.delete("grid")
        for i in range(0, self.CANVAS_WIDTH, self.GRID_SIZE):
            self.canvas.create_line(
                i, 0, i, self.CANVAS_HEIGHT,
                fill=self.colors['grid'], width=1, tags="grid"
            )
        for i in range(0, self.CANVAS_HEIGHT, self.GRID_SIZE):
            self.canvas.create_line(
                0, i, self.CANVAS_WIDTH, i,
                fill=self.colors['grid'], width=1, tags="grid"
            )
            
    def draw_snake(self):
        """Draw the snake with gradient effect"""
        self.canvas.delete("snake")
        
        for i, segment in enumerate(self.snake):
            x1 = segment.x * self.GRID_SIZE
            y1 = segment.y * self.GRID_SIZE
            x2 = x1 + self.GRID_SIZE
            y2 = y1 + self.GRID_SIZE
            
            if i == 0:  # Head
                color = self.colors['snake_head']
                if self.invincible_time > 0:
                    # Flash effect when invincible
                    color = '#ffff00' if self.invincible_time % 4 < 2 else self.colors['snake_head']
            else:  # Body
                # Gradient effect
                intensity = max(0.3, 1 - (i / len(self.snake)))
                green_value = int(255 * intensity)
                color = f"#{0:02x}{green_value:02x}{0:02x}"
                
            self.canvas.create_rectangle(
                x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                fill=color, outline='#004400', width=1, tags="snake"
            )
            
    def draw_food(self):
        """Draw food items"""
        self.canvas.delete("food")
        
        # Regular food
        x1 = self.food.x * self.GRID_SIZE
        y1 = self.food.y * self.GRID_SIZE
        x2 = x1 + self.GRID_SIZE
        y2 = y1 + self.GRID_SIZE
        
        self.canvas.create_oval(
            x1 + 2, y1 + 2, x2 - 2, y2 - 2,
            fill=self.colors['food'], outline='#cc0000', width=2, tags="food"
        )
        
        # Special food
        if self.special_food:
            x1 = self.special_food.x * self.GRID_SIZE
            y1 = self.special_food.y * self.GRID_SIZE
            x2 = x1 + self.GRID_SIZE
            y2 = y1 + self.GRID_SIZE
            
            self.canvas.create_oval(
                x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                fill=self.colors['special_food'], outline='#ffaa00', width=2, tags="food"
            )
            
    def draw_power_ups(self):
        """Draw power-ups"""
        self.canvas.delete("power_up")
        
        for power_up in self.power_ups:
            x1 = power_up.x * self.GRID_SIZE
            y1 = power_up.y * self.GRID_SIZE
            x2 = x1 + self.GRID_SIZE
            y2 = y1 + self.GRID_SIZE
            
            # Draw as a diamond
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            self.canvas.create_polygon(
                center_x, y1 + 2,  # Top
                x2 - 2, center_y,  # Right
                center_x, y2 - 2,  # Bottom
                x1 + 2, center_y,  # Left
                fill=self.colors['power_up'], outline='#cc00cc', width=2, tags="power_up"
            )
            
    def draw_ui(self):
        """Draw UI elements"""
        # Update score and level
        self.score_label.config(text=f"Score: {self.score}")
        self.level_label.config(text=f"Level: {self.level}")
        
        # Draw pause indicator
        if self.state == GameState.PAUSED:
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2,
                self.CANVAS_HEIGHT // 2,
                text="PAUSED\nPress 'P' to continue",
                font=("Arial", 24, "bold"),
                fill='#ffff00',
                justify=tk.CENTER,
                tags="pause"
            )
        else:
            self.canvas.delete("pause")
            
    def game_loop(self):
        """Main game loop"""
        if self.state == GameState.PLAYING:
            self.move_snake()
            self.draw_game()
            self.root.after(self.speed, self.game_loop)
        elif self.state == GameState.PAUSED:
            self.draw_ui()  # Keep drawing pause message
            
    def draw_game(self):
        """Draw all game elements"""
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_food()
        self.draw_power_ups()
        self.draw_snake()
        self.draw_ui()
        
    def run(self):
        """Start the game application"""
        self.root.mainloop()

# Game variations and additional features
class AdvancedSnakeGame(SnakeGame):
    """Extended version with even more features"""
    
    def __init__(self):
        super().__init__()
        self.obstacles = []
        self.multiplier = 1
        self.combo_count = 0
        
    def start_game(self):
        """Override to add obstacles"""
        super().start_game()
        self.create_obstacles()
        
    def create_obstacles(self):
        """Create random obstacles on higher levels"""
        self.obstacles = []
        if self.level >= 3:
            num_obstacles = min(self.level - 2, 8)
            for _ in range(num_obstacles):
                while True:
                    x = random.randint(2, self.GRID_WIDTH - 3)
                    y = random.randint(2, self.GRID_HEIGHT - 3)
                    pos = Point(x, y)
                    
                    if (pos not in self.snake and pos != self.food and 
                        pos not in self.obstacles):
                        self.obstacles.append(pos)
                        break
                        
    def move_snake(self):
        """Override to handle obstacle collisions"""
        if self.state != GameState.PLAYING:
            return
            
        head = self.snake[0]
        new_head = head + self.direction
        
        # Handle wall collision
        new_head.x = new_head.x % self.GRID_WIDTH
        new_head.y = new_head.y % self.GRID_HEIGHT
        
        # Check obstacle collision
        if self.invincible_time <= 0 and new_head in self.obstacles:
            self.game_over()
            return
            
        # Check self collision
        if self.invincible_time <= 0 and new_head in self.snake:
            self.game_over()
            return
            
        # Move snake
        self.snake.insert(0, new_head)
        
        # Food collision logic with combo system
        ate_food = False
        if new_head == self.food:
            self.combo_count += 1
            points = 10 * self.level * self.multiplier
            if self.combo_count > 1:
                points *= self.combo_count  # Combo bonus
            self.score += points
            ate_food = True
            self.place_food()
            
        elif self.special_food and new_head == self.special_food:
            self.combo_count += 1
            points = 50 * self.level * self.multiplier
            if self.combo_count > 1:
                points *= self.combo_count
            self.score += points
            ate_food = True
            self.special_food = None
            
        elif new_head in self.power_ups:
            self.power_ups.remove(new_head)
            self.activate_power_up()
        else:
            self.combo_count = 0  # Reset combo
            
        if not ate_food:
            self.snake.pop()
        else:
            if self.score >= self.level * 200:
                self.level_up()
                
        if self.invincible_time > 0:
            self.invincible_time -= 1
            
    def draw_obstacles(self):
        """Draw obstacles"""
        self.canvas.delete("obstacle")
        
        for obstacle in self.obstacles:
            x1 = obstacle.x * self.GRID_SIZE
            y1 = obstacle.y * self.GRID_SIZE
            x2 = x1 + self.GRID_SIZE
            y2 = y1 + self.GRID_SIZE
            
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill='#666666', outline='#999999', width=2, tags="obstacle"
            )
            
    def draw_game(self):
        """Override to include obstacles"""
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_obstacles()
        self.draw_food()
        self.draw_power_ups()
        self.draw_snake()
        self.draw_ui()
        
        # Draw combo indicator
        if self.combo_count > 1:
            self.canvas.create_text(
                50, 30,
                text=f"COMBO x{self.combo_count}!",
                font=("Arial", 16, "bold"),
                fill='#ffff00',
                tags="ui"
            )
            
    def level_up(self):
        """Override to recreate obstacles"""
        super().level_up()
        self.create_obstacles()

def main():
    """Main function to run the game"""
    try:
        # Check if we want the advanced version
        game = AdvancedSnakeGame()
        
        # Add a welcome message
        print("🐍 Advanced Snake Game Starting...")
        print("Features:")
        print("  • Multiple levels with increasing difficulty")
        print("  • Power-ups and special food")
        print("  • Obstacles on higher levels")
        print("  • Combo system for bonus points")
        print("  • High score tracking")
        print("  • Invincibility power-up")
        print("  • Smooth animations and effects")
        print("\nControls:")
        print("  • WASD or Arrow Keys to move")
        print("  • P to pause/unpause")
        print("  • R to restart (when game over)")
        print("  • ESC to return to menu (when game over)")
        print("\nStarting game...")
        
        game.run()
        
    except KeyboardInterrupt:
        print("\n👋 Thanks for playing!")
    except Exception as e:
        print(f"❌ Error: {e}")
        
if __name__ == "__main__":
    main()