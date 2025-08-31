import tkinter as tk
import random
import time

class TetrisGame:
    def __init__(self):
        # Game window setup
        self.root = tk.Tk()
        self.root.title("Tetris")
        self.root.resizable(False, False)
        
        # Game constants
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 20
        self.CELL_SIZE = 30
        self.CANVAS_WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.CANVAS_HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE
        self.SIDEBAR_WIDTH = 200
        self.TOTAL_WIDTH = self.CANVAS_WIDTH + self.SIDEBAR_WIDTH
        
        # Colors
        self.BG_COLOR = "#1a1a2e"
        self.GRID_COLOR = "#16213e"
        self.BORDER_COLOR = "#374151"
        self.TEXT_COLOR = "#ffffff"
        self.GHOST_COLOR = "#4a5568"
        
        # Tetromino colors
        self.COLORS = {
            'I': "#00f5ff",  # Cyan
            'O': "#ffff00",  # Yellow
            'T': "#800080",  # Purple
            'S': "#00ff00",  # Green
            'Z': "#ff0000",  # Red
            'J': "#0000ff",  # Blue
            'L': "#ffa500"   # Orange
        }
        
        # Tetromino shapes
        self.SHAPES = {
            'I': [['....', 'IIII', '....', '....']],
            'O': [['OO', 'OO']],
            'T': [['...', 'TTT', '.T.'], ['.T.', 'TT.', '.T.'], ['.T.', 'TTT', '...'], ['.T.', '.TT', '.T.']],
            'S': [['...', '.SS', 'SS.'], ['S..', 'SS.', '.S.']],
            'Z': [['...', 'ZZ.', '.ZZ'], ['.Z.', 'ZZ.', 'Z..']],
            'J': [['...', 'JJJ', '..J'], ['JJ.', 'J..', 'J..'], ['J..', 'JJJ', '...'], ['.J.', '.J.', 'JJ.']],
            'L': [['...', 'LLL', 'L..'], ['L..', 'L..', 'LL.'], ['..L', 'LLL', '...'], ['LL.', '.L.', '.L.']]
        }
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.TOTAL_WIDTH,
            height=self.CANVAS_HEIGHT,
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
        self.grid = [[None for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.game_started = False
        self.drop_time = 0
        self.drop_interval = 500  # milliseconds
        
        self.current_piece = None
        self.next_piece = self.get_random_piece()
        self.spawn_piece()
        
    def get_random_piece(self):
        """Get a random tetromino piece"""
        piece_type = random.choice(list(self.SHAPES.keys()))
        return {
            'type': piece_type,
            'shape': self.SHAPES[piece_type][0],
            'rotation': 0,
            'x': self.GRID_WIDTH // 2 - 2,
            'y': 0
        }
    
    def spawn_piece(self):
        """Spawn a new piece"""
        self.current_piece = self.next_piece
        self.next_piece = self.get_random_piece()
        
        # Check if game over
        if self.check_collision(self.current_piece, 0, 0):
            self.game_over = True
    
    def get_piece_cells(self, piece):
        """Get the cells occupied by a piece"""
        cells = []
        shape = self.SHAPES[piece['type']][piece['rotation']]
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell != '.':
                    x = piece['x'] + col_idx
                    y = piece['y'] + row_idx
                    cells.append((x, y))
        
        return cells
    
    def check_collision(self, piece, dx, dy):
        """Check if piece would collide at new position"""
        test_piece = piece.copy()
        test_piece['x'] += dx
        test_piece['y'] += dy
        
        cells = self.get_piece_cells(test_piece)
        
        for x, y in cells:
            # Check boundaries
            if x < 0 or x >= self.GRID_WIDTH or y >= self.GRID_HEIGHT:
                return True
            
            # Check collision with placed pieces
            if y >= 0 and self.grid[y][x] is not None:
                return True
        
        return False
    
    def rotate_piece(self, piece):
        """Rotate piece clockwise"""
        new_piece = piece.copy()
        max_rotations = len(self.SHAPES[piece['type']])
        new_piece['rotation'] = (piece['rotation'] + 1) % max_rotations
        new_piece['shape'] = self.SHAPES[piece['type']][new_piece['rotation']]
        
        return new_piece
    
    def move_piece(self, dx, dy):
        """Move current piece if possible"""
        if self.current_piece and not self.game_over:
            if not self.check_collision(self.current_piece, dx, dy):
                self.current_piece['x'] += dx
                self.current_piece['y'] += dy
                return True
        return False
    
    def rotate_current_piece(self):
        """Rotate current piece if possible"""
        if self.current_piece and not self.game_over:
            rotated = self.rotate_piece(self.current_piece)
            if not self.check_collision(rotated, 0, 0):
                self.current_piece = rotated
                return True
        return False
    
    def lock_piece(self):
        """Lock current piece in place"""
        if not self.current_piece:
            return
            
        cells = self.get_piece_cells(self.current_piece)
        piece_type = self.current_piece['type']
        
        for x, y in cells:
            if y >= 0:
                self.grid[y][x] = piece_type
        
        # Check for completed lines
        self.clear_lines()
        
        # Spawn next piece
        self.spawn_piece()
    
    def clear_lines(self):
        """Clear completed lines and update score"""
        lines_to_clear = []
        
        for y in range(self.GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        # Remove completed lines
        for y in sorted(lines_to_clear, reverse=True):
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(self.GRID_WIDTH)])
        
        # Update score and level
        lines_count = len(lines_to_clear)
        if lines_count > 0:
            # Scoring system
            line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += line_scores.get(lines_count, 0) * self.level
            self.lines_cleared += lines_count
            
            # Level up every 10 lines
            new_level = (self.lines_cleared // 10) + 1
            if new_level > self.level:
                self.level = new_level
                self.drop_interval = max(50, 500 - (self.level - 1) * 50)
    
    def drop_piece(self):
        """Drop current piece one row"""
        if not self.move_piece(0, 1):
            self.lock_piece()
    
    def hard_drop(self):
        """Drop piece to bottom instantly"""
        if self.current_piece and not self.game_over:
            while self.move_piece(0, 1):
                self.score += 2  # Bonus points for hard drop
    
    def get_ghost_piece(self):
        """Get ghost piece position (where piece would land)"""
        if not self.current_piece:
            return None
            
        ghost = self.current_piece.copy()
        while not self.check_collision(ghost, 0, 1):
            ghost['y'] += 1
        
        return ghost
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.keysym.lower()
        
        if self.game_over:
            if key in ['space', 'return']:
                self.reset_game()
            return
        
        if not self.game_started:
            self.game_started = True
        
        # Movement controls
        if key in ['left', 'a']:
            self.move_piece(-1, 0)
        elif key in ['right', 'd']:
            self.move_piece(1, 0)
        elif key in ['down', 's']:
            if self.move_piece(0, 1):
                self.score += 1  # Bonus point for soft drop
        elif key in ['up', 'w', 'space']:
            self.rotate_current_piece()
        elif key == 'q':
            self.hard_drop()
    
    def draw_cell(self, x, y, color, alpha=1.0):
        """Draw a single cell"""
        pixel_x = x * self.CELL_SIZE
        pixel_y = y * self.CELL_SIZE
        
        if alpha < 1.0:
            # Draw ghost piece with transparency effect
            self.canvas.create_rectangle(
                pixel_x + 2, pixel_y + 2,
                pixel_x + self.CELL_SIZE - 2, pixel_y + self.CELL_SIZE - 2,
                fill="",
                outline=color,
                width=2,
                stipple="gray50"
            )
        else:
            # Draw solid piece
            self.canvas.create_rectangle(
                pixel_x + 1, pixel_y + 1,
                pixel_x + self.CELL_SIZE - 1, pixel_y + self.CELL_SIZE - 1,
                fill=color,
                outline="#ffffff",
                width=1
            )
            
            # Add highlight for 3D effect
            self.canvas.create_line(
                pixel_x + 1, pixel_y + 1,
                pixel_x + self.CELL_SIZE - 1, pixel_y + 1,
                fill="#ffffff",
                width=2
            )
            self.canvas.create_line(
                pixel_x + 1, pixel_y + 1,
                pixel_x + 1, pixel_y + self.CELL_SIZE - 1,
                fill="#ffffff",
                width=2
            )
    
    def draw_grid(self):
        """Draw the game grid"""
        # Draw grid lines
        for x in range(self.GRID_WIDTH + 1):
            pixel_x = x * self.CELL_SIZE
            self.canvas.create_line(
                pixel_x, 0, pixel_x, self.CANVAS_HEIGHT,
                fill=self.GRID_COLOR,
                width=1
            )
        
        for y in range(self.GRID_HEIGHT + 1):
            pixel_y = y * self.CELL_SIZE
            self.canvas.create_line(
                0, pixel_y, self.CANVAS_WIDTH, pixel_y,
                fill=self.GRID_COLOR,
                width=1
            )
        
        # Draw border
        self.canvas.create_rectangle(
            0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT,
            fill="",
            outline=self.BORDER_COLOR,
            width=3
        )
    
    def draw_placed_pieces(self):
        """Draw all placed pieces on the grid"""
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                if self.grid[y][x] is not None:
                    color = self.COLORS[self.grid[y][x]]
                    self.draw_cell(x, y, color)
    
    def draw_current_piece(self):
        """Draw the current falling piece"""
        if not self.current_piece:
            return
        
        # Draw ghost piece first
        ghost = self.get_ghost_piece()
        if ghost and ghost['y'] != self.current_piece['y']:
            ghost_cells = self.get_piece_cells(ghost)
            ghost_color = self.COLORS[ghost['type']]
            for x, y in ghost_cells:
                if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
                    self.draw_cell(x, y, ghost_color, alpha=0.3)
        
        # Draw current piece
        cells = self.get_piece_cells(self.current_piece)
        color = self.COLORS[self.current_piece['type']]
        
        for x, y in cells:
            if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
                self.draw_cell(x, y, color)
    
    def draw_next_piece(self):
        """Draw the next piece preview"""
        if not self.next_piece:
            return
        
        # Clear next piece area
        start_x = self.CANVAS_WIDTH + 20
        start_y = 100
        
        self.canvas.create_rectangle(
            start_x - 10, start_y - 10,
            start_x + 120, start_y + 120,
            fill=self.BG_COLOR,
            outline=self.BORDER_COLOR,
            width=2
        )
        
        self.canvas.create_text(
            start_x + 50, start_y - 30,
            text="NEXT",
            font=("Courier", 14, "bold"),
            fill=self.TEXT_COLOR,
            anchor="center"
        )
        
        # Draw next piece
        shape = self.SHAPES[self.next_piece['type']][0]
        color = self.COLORS[self.next_piece['type']]
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell != '.':
                    x = start_x + col_idx * 25
                    y = start_y + row_idx * 25
                    
                    self.canvas.create_rectangle(
                        x, y, x + 23, y + 23,
                        fill=color,
                        outline="#ffffff",
                        width=1
                    )
    
    def draw_stats(self):
        """Draw game statistics"""
        start_x = self.CANVAS_WIDTH + 20
        start_y = 250
        
        stats = [
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Lines: {self.lines_cleared}",
        ]
        
        for i, stat in enumerate(stats):
            self.canvas.create_text(
                start_x, start_y + i * 30,
                text=stat,
                font=("Courier", 12, "bold"),
                fill=self.TEXT_COLOR,
                anchor="nw"
            )
    
    def draw_controls(self):
        """Draw control instructions"""
        start_x = self.CANVAS_WIDTH + 20
        start_y = 400
        
        self.canvas.create_text(
            start_x, start_y,
            text="CONTROLS",
            font=("Courier", 12, "bold"),
            fill=self.TEXT_COLOR,
            anchor="nw"
        )
        
        controls = [
            "← → : Move",
            "↓ : Soft Drop",
            "↑ : Rotate",
            "Q : Hard Drop",
            "Space: Rotate"
        ]
        
        for i, control in enumerate(controls):
            self.canvas.create_text(
                start_x, start_y + 25 + i * 20,
                text=control,
                font=("Courier", 9),
                fill="#94a3b8",
                anchor="nw"
            )
    
    def draw_instructions(self):
        """Draw game instructions"""
        if not self.game_started:
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 - 100,
                text="TETRIS",
                font=("Courier", 32, "bold"),
                fill="#00f5ff",
                anchor="center"
            )
            
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 - 50,
                text="Press any key to start",
                font=("Courier", 14),
                fill=self.TEXT_COLOR,
                anchor="center"
            )
    
    def draw_game_over(self):
        """Draw game over screen"""
        if self.game_over:
            # Semi-transparent overlay
            self.canvas.create_rectangle(
                0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT,
                fill="#000000",
                stipple="gray50"
            )
            
            # Game over text
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 - 60,
                text="GAME OVER",
                font=("Courier", 24, "bold"),
                fill="#ef4444",
                anchor="center"
            )
            
            # Final score
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 - 20,
                text=f"Final Score: {self.score}",
                font=("Courier", 16),
                fill=self.TEXT_COLOR,
                anchor="center"
            )
            
            # Level reached
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 10,
                text=f"Level Reached: {self.level}",
                font=("Courier", 12),
                fill="#94a3b8",
                anchor="center"
            )
            
            # Restart instruction
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 50,
                text="Press SPACE or ENTER to restart",
                font=("Courier", 12),
                fill=self.TEXT_COLOR,
                anchor="center"
            )
    
    def draw_everything(self):
        """Draw all game elements"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw game area
        self.draw_grid()
        self.draw_placed_pieces()
        
        if self.game_started:
            self.draw_current_piece()
        
        # Draw sidebar
        self.draw_next_piece()
        self.draw_stats()
        self.draw_controls()
        
        if not self.game_started:
            self.draw_instructions()
        
        if self.game_over:
            self.draw_game_over()
    
    def update_game(self):
        """Update game state"""
        if not self.game_started or self.game_over:
            return
        
        current_time = int(time.time() * 1000)
        
        if current_time - self.drop_time >= self.drop_interval:
            self.drop_piece()
            self.drop_time = current_time
    
    def game_loop(self):
        """Main game loop"""
        self.update_game()
        self.draw_everything()
        
        # Schedule next frame
        self.root.after(16, self.game_loop)  # ~60 FPS
    
    def run(self):
        """Start the game"""
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.TOTAL_WIDTH) // 2
        y = (self.root.winfo_screenheight() - self.CANVAS_HEIGHT) // 2
        self.root.geometry(f"{self.TOTAL_WIDTH}x{self.CANVAS_HEIGHT}+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()