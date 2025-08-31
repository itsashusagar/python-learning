#!/usr/bin/env python3
"""
Complete Ludo Game Implementation in Pygame
A single-file implementation of the classic Ludo board game.
"""

import pygame
import random
import math
import sys
from enum import Enum
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 53, 69)
BLUE = (13, 110, 253)
GREEN = (25, 135, 84)
YELLOW = (255, 193, 7)
LIGHT_GRAY = (248, 249, 250)
DARK_GRAY = (108, 117, 125)
BOARD_COLOR = (245, 245, 245)

# Board dimensions
BOARD_SIZE = 600
BOARD_OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_OFFSET_Y = 50
CELL_SIZE = BOARD_SIZE // 15

# Dice settings
DICE_SIZE = 60
DICE_X = SCREEN_WIDTH // 2 - DICE_SIZE // 2
DICE_Y = SCREEN_HEIGHT - 100

class PlayerColor(Enum):
    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3

class TokenState(Enum):
    HOME = 0
    ON_BOARD = 1
    FINISHED = 2

class Token:
    """Represents a single game token."""
    
    def __init__(self, color: PlayerColor, token_id: int):
        self.color = color
        self.token_id = token_id
        self.state = TokenState.HOME
        self.position = -1  # -1 means in home
        self.board_position = 0  # Position on the main track (0-51)
        self.home_lane_position = -1  # Position in home lane (0-5)
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.animation_speed = 8
        
    def get_color_rgb(self) -> Tuple[int, int, int]:
        """Get RGB color for this token."""
        color_map = {
            PlayerColor.RED: RED,
            PlayerColor.BLUE: BLUE,
            PlayerColor.GREEN: GREEN,
            PlayerColor.YELLOW: YELLOW
        }
        return color_map[self.color]
    
    def update_animation(self):
        """Update token position animation."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        if abs(dx) < 1 and abs(dy) < 1:
            self.x = self.target_x
            self.y = self.target_y
        else:
            self.x += dx * 0.15
            self.y += dy * 0.15

class LudoBoard:
    """Manages the Ludo board layout and rendering."""
    
    def __init__(self):
        self.board_positions = self._calculate_board_positions()
        self.home_positions = self._calculate_home_positions()
        self.home_lane_positions = self._calculate_home_lane_positions()
        
    def _calculate_board_positions(self) -> List[Tuple[int, int]]:
        """Calculate all 52 positions on the main board track."""
        positions = []
        
        # Bottom row (left to right, positions 0-5)
        for i in range(6):
            x = BOARD_OFFSET_X + i * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + 8 * CELL_SIZE + CELL_SIZE // 2
            positions.append((x, y))
            
        # Left column (bottom to top, positions 6-11)
        for i in range(6):
            x = BOARD_OFFSET_X + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + (7 - i) * CELL_SIZE + CELL_SIZE // 2
            positions.append((x, y))
            
        # Top row (left to right, positions 12-17)
        for i in range(6):
            x = BOARD_OFFSET_X + (i + 1) * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + CELL_SIZE // 2
            positions.append((x, y))
            
        # Right column top part (top to bottom, positions 18-23)
        for i in range(6):
            x = BOARD_OFFSET_X + 7 * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + (i + 1) * CELL_SIZE + CELL_SIZE // 2
            positions.append((x, y))
            
        # Top row right part (left to right, positions 24-29)
        for i in range(6):
            x = BOARD_OFFSET_X + (8 + i) * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + CELL_SIZE // 2
            positions.append((x, y))
            
        # Right column (top to bottom, positions 30-35)
        for i in range(6):
            x = BOARD_OFFSET_X + 14 * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + (i + 1) * CELL_SIZE + CELL_SIZE // 2
            positions.append((x, y))
            
        # Bottom row right part (right to left, positions 36-41)
        for i in range(6):
            x = BOARD_OFFSET_X + (13 - i) * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + 7 * CELL_SIZE + CELL_SIZE // 2
            positions.append((x, y))
            
        # Right column bottom part (bottom to top, positions 42-47)
        for i in range(6):
            x = BOARD_OFFSET_X + 7 * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + (7 - i) * CELL_SIZE + CELL_SIZE // 2
            positions.append((x, y))
            
        # Bottom row left part (right to left, positions 48-51)
        for i in range(4):
            x = BOARD_OFFSET_X + (6 - i) * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + 8 * CELL_SIZE + CELL_SIZE // 2
            positions.append((x, y))
            
        return positions
    
    def _calculate_home_positions(self) -> dict:
        """Calculate home positions for each player's tokens."""
        home_positions = {}
        
        # Red home (bottom-left)
        red_home = []
        for row in range(2):
            for col in range(2):
                x = BOARD_OFFSET_X + (1 + col) * CELL_SIZE + CELL_SIZE // 2
                y = BOARD_OFFSET_Y + (10 + row) * CELL_SIZE + CELL_SIZE // 2
                red_home.append((x, y))
        home_positions[PlayerColor.RED] = red_home
        
        # Blue home (top-left)
        blue_home = []
        for row in range(2):
            for col in range(2):
                x = BOARD_OFFSET_X + (1 + col) * CELL_SIZE + CELL_SIZE // 2
                y = BOARD_OFFSET_Y + (3 + row) * CELL_SIZE + CELL_SIZE // 2
                blue_home.append((x, y))
        home_positions[PlayerColor.BLUE] = blue_home
        
        # Green home (top-right)
        green_home = []
        for row in range(2):
            for col in range(2):
                x = BOARD_OFFSET_X + (12 + col) * CELL_SIZE + CELL_SIZE // 2
                y = BOARD_OFFSET_Y + (3 + row) * CELL_SIZE + CELL_SIZE // 2
                green_home.append((x, y))
        home_positions[PlayerColor.GREEN] = green_home
        
        # Yellow home (bottom-right)
        yellow_home = []
        for row in range(2):
            for col in range(2):
                x = BOARD_OFFSET_X + (12 + col) * CELL_SIZE + CELL_SIZE // 2
                y = BOARD_OFFSET_Y + (10 + row) * CELL_SIZE + CELL_SIZE // 2
                yellow_home.append((x, y))
        home_positions[PlayerColor.YELLOW] = yellow_home
        
        return home_positions
    
    def _calculate_home_lane_positions(self) -> dict:
        """Calculate home lane positions for each player."""
        home_lanes = {}
        
        # Red home lane (vertical, going up)
        red_lane = []
        for i in range(6):
            x = BOARD_OFFSET_X + CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + (8 - i) * CELL_SIZE + CELL_SIZE // 2
            red_lane.append((x, y))
        home_lanes[PlayerColor.RED] = red_lane
        
        # Blue home lane (horizontal, going right)
        blue_lane = []
        for i in range(6):
            x = BOARD_OFFSET_X + (1 + i) * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + CELL_SIZE + CELL_SIZE // 2
            blue_lane.append((x, y))
        home_lanes[PlayerColor.BLUE] = blue_lane
        
        # Green home lane (vertical, going down)
        green_lane = []
        for i in range(6):
            x = BOARD_OFFSET_X + 13 * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + (1 + i) * CELL_SIZE + CELL_SIZE // 2
            green_lane.append((x, y))
        home_lanes[PlayerColor.GREEN] = green_lane
        
        # Yellow home lane (horizontal, going left)
        yellow_lane = []
        for i in range(6):
            x = BOARD_OFFSET_X + (13 - i) * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + 13 * CELL_SIZE + CELL_SIZE // 2
            yellow_lane.append((x, y))
        home_lanes[PlayerColor.YELLOW] = yellow_lane
        
        return home_lanes

class Dice:
    """Manages dice rolling and animation."""
    
    def __init__(self):
        self.value = 1
        self.rolling = False
        self.roll_timer = 0
        self.roll_duration = 30  # frames
        
    def roll(self):
        """Start rolling the dice."""
        if not self.rolling:
            self.rolling = True
            self.roll_timer = 0
            
    def update(self):
        """Update dice animation."""
        if self.rolling:
            self.roll_timer += 1
            self.value = random.randint(1, 6)
            
            if self.roll_timer >= self.roll_duration:
                self.rolling = False
                self.value = random.randint(1, 6)
                
    def draw(self, screen, font):
        """Draw the dice."""
        # Draw dice background
        dice_rect = pygame.Rect(DICE_X, DICE_Y, DICE_SIZE, DICE_SIZE)
        pygame.draw.rect(screen, WHITE, dice_rect)
        pygame.draw.rect(screen, BLACK, dice_rect, 3)
        
        # Draw dice dots
        self._draw_dice_dots(screen, self.value)
        
        # Draw roll button
        button_rect = pygame.Rect(DICE_X - 30, DICE_Y + 80, DICE_SIZE + 60, 30)
        button_color = LIGHT_GRAY if self.rolling else WHITE
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 2)
        
        button_text = "Rolling..." if self.rolling else "Roll Dice"
        text_surface = font.render(button_text, True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        
    def _draw_dice_dots(self, screen, value):
        """Draw dots on the dice face."""
        dot_radius = 6
        center_x = DICE_X + DICE_SIZE // 2
        center_y = DICE_Y + DICE_SIZE // 2
        
        # Dot positions relative to center
        dot_positions = {
            1: [(0, 0)],
            2: [(-15, -15), (15, 15)],
            3: [(-15, -15), (0, 0), (15, 15)],
            4: [(-15, -15), (15, -15), (-15, 15), (15, 15)],
            5: [(-15, -15), (15, -15), (0, 0), (-15, 15), (15, 15)],
            6: [(-15, -15), (15, -15), (-15, 0), (15, 0), (-15, 15), (15, 15)]
        }
        
        for dx, dy in dot_positions[value]:
            pygame.draw.circle(screen, BLACK, (center_x + dx, center_y + dy), dot_radius)
    
    def get_roll_button_rect(self):
        """Get the rectangle for the roll button."""
        return pygame.Rect(DICE_X - 30, DICE_Y + 80, DICE_SIZE + 60, 30)

class LudoGame:
    """Main Ludo game class."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ludo Game")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        
        # Game state
        self.current_player = PlayerColor.RED
        self.dice = Dice()
        self.board = LudoBoard()
        self.tokens = self._initialize_tokens()
        self.game_over = False
        self.winner = None
        self.dice_rolled = False
        self.can_move = False
        self.valid_tokens = []
        
        # Starting positions for each color
        self.start_positions = {
            PlayerColor.RED: 0,
            PlayerColor.BLUE: 13,
            PlayerColor.GREEN: 26,
            PlayerColor.YELLOW: 39
        }
        
        # Safe positions (where tokens can't be captured)
        self.safe_positions = {0, 8, 13, 21, 26, 34, 39, 47}
        
        self._update_token_positions()
    
    def _initialize_tokens(self) -> dict:
        """Initialize all player tokens."""
        tokens = {}
        for color in PlayerColor:
            tokens[color] = [Token(color, i) for i in range(4)]
        return tokens
    
    def _update_token_positions(self):
        """Update visual positions of all tokens."""
        for color in PlayerColor:
            for i, token in enumerate(self.tokens[color]):
                if token.state == TokenState.HOME:
                    pos = self.board.home_positions[color][i]
                    token.target_x, token.target_y = pos
                elif token.state == TokenState.FINISHED:
                    # Token is in the center finish area
                    center_x = BOARD_OFFSET_X + BOARD_SIZE // 2
                    center_y = BOARD_OFFSET_Y + BOARD_SIZE // 2
                    # Arrange finished tokens in a small grid
                    offset_x = (i % 2 - 0.5) * 15
                    offset_y = (i // 2 - 0.5) * 15
                    token.target_x = center_x + offset_x
                    token.target_y = center_y + offset_y
                elif token.home_lane_position >= 0:
                    # Token is in home lane
                    pos = self.board.home_lane_positions[color][token.home_lane_position]
                    token.target_x, token.target_y = pos
                else:
                    # Token is on main board
                    pos = self.board.board_positions[token.board_position]
                    token.target_x, token.target_y = pos
    
    def _get_valid_tokens(self, dice_value: int) -> List[Token]:
        """Get list of tokens that can be moved with the current dice value."""
        valid_tokens = []
        current_tokens = self.tokens[self.current_player]
        
        for token in current_tokens:
            if token.state == TokenState.HOME:
                # Can only move out of home with a 6
                if dice_value == 6:
                    valid_tokens.append(token)
            elif token.state == TokenState.ON_BOARD:
                # Check if token can move without overshooting
                if token.home_lane_position >= 0:
                    # Token is in home lane
                    if token.home_lane_position + dice_value <= 6:
                        valid_tokens.append(token)
                else:
                    # Token is on main board
                    steps_to_home = 51 - token.board_position
                    if steps_to_home > dice_value:
                        valid_tokens.append(token)
                    elif steps_to_home == dice_value:
                        # Can enter home lane
                        valid_tokens.append(token)
                    elif steps_to_home + dice_value <= 6:
                        # Can move in home lane
                        valid_tokens.append(token)
        
        return valid_tokens
    
    def _move_token(self, token: Token, dice_value: int):
        """Move a token based on dice value."""
        if token.state == TokenState.HOME:
            # Move token out of home
            token.state = TokenState.ON_BOARD
            token.board_position = self.start_positions[token.color]
            token.position = 0
        elif token.home_lane_position >= 0:
            # Token is in home lane
            token.home_lane_position += dice_value
            if token.home_lane_position >= 6:
                token.state = TokenState.FINISHED
                token.home_lane_position = -1
        else:
            # Token is on main board
            new_position = token.board_position + dice_value
            
            if new_position >= 52:
                # Wrap around the board
                new_position -= 52
            
            # Check if token should enter home lane
            start_pos = self.start_positions[token.color]
            steps_from_start = (new_position - start_pos) % 52
            
            if steps_from_start >= 51:
                # Enter home lane
                steps_in_lane = steps_from_start - 51
                if steps_in_lane < 6:
                    token.home_lane_position = steps_in_lane
                else:
                    token.state = TokenState.FINISHED
            else:
                token.board_position = new_position
                
                # Check for captures
                self._check_capture(token)
        
        self._update_token_positions()
    
    def _check_capture(self, moved_token: Token):
        """Check if the moved token captures any opponent tokens."""
        if moved_token.board_position in self.safe_positions:
            return  # Can't capture on safe positions
            
        for color in PlayerColor:
            if color == moved_token.color:
                continue
                
            for token in self.tokens[color]:
                if (token.state == TokenState.ON_BOARD and 
                    token.home_lane_position < 0 and
                    token.board_position == moved_token.board_position):
                    # Capture the token
                    token.state = TokenState.HOME
                    token.board_position = 0
                    token.position = -1
        
        self._update_token_positions()
    
    def _check_win_condition(self) -> bool:
        """Check if current player has won."""
        for token in self.tokens[self.current_player]:
            if token.state != TokenState.FINISHED:
                return False
        return True
    
    def _next_player(self):
        """Move to the next player."""
        players = list(PlayerColor)
        current_index = players.index(self.current_player)
        self.current_player = players[(current_index + 1) % 4]
        self.dice_rolled = False
        self.can_move = False
        self.valid_tokens = []
    
    def _get_player_name(self, color: PlayerColor) -> str:
        """Get display name for player color."""
        return color.name.title()
    
    def _get_token_at_position(self, pos: Tuple[int, int]) -> Optional[Token]:
        """Get token at the given screen position."""
        for color in PlayerColor:
            for token in self.tokens[color]:
                distance = math.sqrt((token.x - pos[0])**2 + (token.y - pos[1])**2)
                if distance < 20:  # Token radius
                    return token
        return None
    
    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click events."""
        # Check dice roll button
        if self.dice.get_roll_button_rect().collidepoint(pos) and not self.dice_rolled:
            self.dice.roll()
            self.dice_rolled = True
            return
        
        # Check if dice finished rolling
        if self.dice_rolled and not self.dice.rolling and not self.can_move:
            self.valid_tokens = self._get_valid_tokens(self.dice.value)
            self.can_move = True
            
            # If no valid moves, skip turn
            if not self.valid_tokens:
                if self.dice.value != 6:
                    self._next_player()
                else:
                    self.dice_rolled = False
                    self.can_move = False
                return
        
        # Handle token selection
        if self.can_move and self.valid_tokens:
            clicked_token = self._get_token_at_position(pos)
            if clicked_token and clicked_token in self.valid_tokens:
                self._move_token(clicked_token, self.dice.value)
                
                # Check win condition
                if self._check_win_condition():
                    self.game_over = True
                    self.winner = self.current_player
                
                # Next turn (extra turn for rolling 6)
                if self.dice.value != 6:
                    self._next_player()
                else:
                    self.dice_rolled = False
                    self.can_move = False
                    self.valid_tokens = []
    
    def draw_board(self):
        """Draw the Ludo board."""
        # Draw board background
        board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE)
        pygame.draw.rect(self.screen, BOARD_COLOR, board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 3)
        
        # Draw grid lines
        for i in range(16):
            # Vertical lines
            x = BOARD_OFFSET_X + i * CELL_SIZE
            pygame.draw.line(self.screen, DARK_GRAY, (x, BOARD_OFFSET_Y), (x, BOARD_OFFSET_Y + BOARD_SIZE), 1)
            
            # Horizontal lines
            y = BOARD_OFFSET_Y + i * CELL_SIZE
            pygame.draw.line(self.screen, DARK_GRAY, (BOARD_OFFSET_X, y), (BOARD_OFFSET_X + BOARD_SIZE, y), 1)
        
        # Draw colored home areas
        self._draw_home_areas()
        
        # Draw safe positions
        self._draw_safe_positions()
        
        # Draw home lanes
        self._draw_home_lanes()
        
        # Draw center area
        center_rect = pygame.Rect(
            BOARD_OFFSET_X + 6 * CELL_SIZE,
            BOARD_OFFSET_Y + 6 * CELL_SIZE,
            3 * CELL_SIZE,
            3 * CELL_SIZE
        )
        pygame.draw.rect(self.screen, WHITE, center_rect)
        pygame.draw.rect(self.screen, BLACK, center_rect, 2)
    
    def _draw_home_areas(self):
        """Draw the colored home areas."""
        home_areas = [
            (RED, 0, 9, 6, 6),      # Red home
            (BLUE, 0, 0, 6, 6),     # Blue home
            (GREEN, 9, 0, 6, 6),    # Green home
            (YELLOW, 9, 9, 6, 6)    # Yellow home
        ]
        
        for color, grid_x, grid_y, width, height in home_areas:
            rect = pygame.Rect(
                BOARD_OFFSET_X + grid_x * CELL_SIZE,
                BOARD_OFFSET_Y + grid_y * CELL_SIZE,
                width * CELL_SIZE,
                height * CELL_SIZE
            )
            pygame.draw.rect(self.screen, (*color, 100), rect)
            pygame.draw.rect(self.screen, color, rect, 3)
    
    def _draw_safe_positions(self):
        """Draw safe positions on the board."""
        safe_board_positions = [0, 8, 13, 21, 26, 34, 39, 47]
        
        for pos in safe_board_positions:
            if pos < len(self.board.board_positions):
                x, y = self.board.board_positions[pos]
                pygame.draw.circle(self.screen, BLACK, (int(x), int(y)), 25, 3)
    
    def _draw_home_lanes(self):
        """Draw the home lanes."""
        # Red home lane (vertical)
        for i in range(6):
            rect = pygame.Rect(
                BOARD_OFFSET_X + CELL_SIZE,
                BOARD_OFFSET_Y + (2 + i) * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, (*RED, 150), rect)
        
        # Blue home lane (horizontal)
        for i in range(6):
            rect = pygame.Rect(
                BOARD_OFFSET_X + (1 + i) * CELL_SIZE,
                BOARD_OFFSET_Y + CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, (*BLUE, 150), rect)
        
        # Green home lane (vertical)
        for i in range(6):
            rect = pygame.Rect(
                BOARD_OFFSET_X + 13 * CELL_SIZE,
                BOARD_OFFSET_Y + (1 + i) * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, (*GREEN, 150), rect)
        
        # Yellow home lane (horizontal)
        for i in range(6):
            rect = pygame.Rect(
                BOARD_OFFSET_X + (8 + i) * CELL_SIZE,
                BOARD_OFFSET_Y + 13 * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, (*YELLOW, 150), rect)
    
    def draw_tokens(self):
        """Draw all tokens."""
        for color in PlayerColor:
            for token in self.tokens[color]:
                # Update animation
                token.update_animation()
                
                # Highlight valid tokens
                is_valid = token in self.valid_tokens
                radius = 18 if is_valid else 15
                
                if is_valid:
                    # Draw highlight ring
                    pygame.draw.circle(self.screen, WHITE, (int(token.x), int(token.y)), radius + 3)
                
                # Draw token
                pygame.draw.circle(self.screen, token.get_color_rgb(), (int(token.x), int(token.y)), radius)
                pygame.draw.circle(self.screen, BLACK, (int(token.x), int(token.y)), radius, 2)
                
                # Draw token number
                text = self.font.render(str(token.token_id + 1), True, WHITE)
                text_rect = text.get_rect(center=(int(token.x), int(token.y)))
                self.screen.blit(text, text_rect)
    
    def draw_ui(self):
        """Draw the user interface."""
        # Title
        title_text = self.title_font.render("LUDO GAME", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 25))
        self.screen.blit(title_text, title_rect)
        
        # Current player indicator
        if not self.game_over:
            player_name = self._get_player_name(self.current_player)
            player_text = self.font.render(f"Current Player: {player_name}", True, BLACK)
            self.screen.blit(player_text, (20, SCREEN_HEIGHT - 150))
            
            # Draw player color indicator
            color_rect = pygame.Rect(200, SCREEN_HEIGHT - 155, 30, 20)
            player_colors = {
                PlayerColor.RED: RED,
                PlayerColor.BLUE: BLUE,
                PlayerColor.GREEN: GREEN,
                PlayerColor.YELLOW: YELLOW
            }
            pygame.draw.rect(self.screen, player_colors[self.current_player], color_rect)
            pygame.draw.rect(self.screen, BLACK, color_rect, 2)
            
            # Game instructions
            if not self.dice_rolled:
                instruction = "Click 'Roll Dice' to roll"
            elif self.dice.rolling:
                instruction = "Rolling dice..."
            elif self.can_move and self.valid_tokens:
                instruction = f"Click a highlighted token to move {self.dice.value} steps"
            elif self.can_move and not self.valid_tokens:
                instruction = "No valid moves available - turn skipped"
            else:
                instruction = "Waiting for dice roll"
                
            inst_text = self.font.render(instruction, True, BLACK)
            self.screen.blit(inst_text, (20, SCREEN_HEIGHT - 125))
        
        # Game over screen
        if self.game_over and self.winner:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Winner announcement
            winner_name = self._get_player_name(self.winner)
            win_text = self.title_font.render(f"{winner_name} Wins!", True, WHITE)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(win_text, win_rect)
            
            # Restart instruction
            restart_text = self.font.render("Press R to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        """Restart the game."""
        self.current_player = PlayerColor.RED
        self.dice = Dice()
        self.tokens = self._initialize_tokens()
        self.game_over = False
        self.winner = None
        self.dice_rolled = False
        self.can_move = False
        self.valid_tokens = []
        self._update_token_positions()
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_over:
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.restart_game()
                        elif event.key == pygame.K_ESCAPE:
                            running = False
            
            # Update game state
            self.dice.update()
            
            # Check if dice finished rolling and enable movement
            if (self.dice_rolled and not self.dice.rolling and not self.can_move):
                self.valid_tokens = self._get_valid_tokens(self.dice.value)
                self.can_move = True
                
                # Auto-skip turn if no valid moves and not a 6
                if not self.valid_tokens and self.dice.value != 6:
                    self._next_player()
            
            # Draw everything
            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_tokens()
            self.dice.draw(self.screen, self.font)
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    """Main entry point."""
    try:
        game = LudoGame()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())