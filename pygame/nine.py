#!/usr/bin/env python3
"""
Advanced Space Shooter Game
A sophisticated space combat game with multiple enemy types, power-ups, and boss battles.
"""

import tkinter as tk
from tkinter import messagebox
import random
import math
import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json
import os

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    BOSS_BATTLE = "boss_battle"

class EnemyType(Enum):
    BASIC = "basic"
    FAST = "fast"
    HEAVY = "heavy"
    BOMBER = "bomber"
    BOSS = "boss"

@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class GameObject:
    def __init__(self, pos: Vector2, size: float, color: str):
        self.pos = pos
        self.size = size
        self.color = color
        self.velocity = Vector2(0, 0)
        self.health = 1
        self.active = True
        
    def update(self, dt: float):
        self.pos = self.pos + self.velocity * dt
        
    def collides_with(self, other) -> bool:
        distance = self.pos.distance_to(other.pos)
        return distance < (self.size + other.size) / 2

class Player(GameObject):
    def __init__(self, pos: Vector2):
        super().__init__(pos, 20, '#00ff00')
        self.health = 100
        self.max_health = 100
        self.speed = 300
        self.shoot_cooldown = 0
        self.power_level = 1
        self.shield = 0
        
    def update(self, dt: float):
        super().update(dt)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.shield > 0:
            self.shield -= dt

class Bullet(GameObject):
    def __init__(self, pos: Vector2, velocity: Vector2, color: str = '#ffff00', damage: int = 1):
        super().__init__(pos, 4, color)
        self.velocity = velocity
        self.damage = damage

class Enemy(GameObject):
    def __init__(self, pos: Vector2, enemy_type: EnemyType):
        self.type = enemy_type
        self.shoot_cooldown = 0
        self.points = 10
        
        if enemy_type == EnemyType.BASIC:
            super().__init__(pos, 15, '#ff0000')
            self.health = 1
            self.speed = 100
            self.points = 10
        elif enemy_type == EnemyType.FAST:
            super().__init__(pos, 12, '#ff8800')
            self.health = 1
            self.speed = 200
            self.points = 20
        elif enemy_type == EnemyType.HEAVY:
            super().__init__(pos, 25, '#8800ff')
            self.health = 3
            self.speed = 50
            self.points = 50
        elif enemy_type == EnemyType.BOMBER:
            super().__init__(pos, 18, '#ff0088')
            self.health = 2
            self.speed = 80
            self.points = 30
        elif enemy_type == EnemyType.BOSS:
            super().__init__(pos, 60, '#ff0000')
            self.health = 50
            self.speed = 30
            self.points = 500
            
    def update(self, dt: float, player_pos: Vector2):
        super().update(dt)
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
            
        # Basic AI movement
        if self.type == EnemyType.BASIC:
            self.velocity = Vector2(0, self.speed)
        elif self.type == EnemyType.FAST:
            # Move toward player
            dx = player_pos.x - self.pos.x
            dy = player_pos.y - self.pos.y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0:
                self.velocity = Vector2(dx/distance * self.speed, dy/distance * self.speed)
        elif self.type == EnemyType.HEAVY:
            self.velocity = Vector2(0, self.speed)
        elif self.type == EnemyType.BOMBER:
            # Zigzag pattern
            self.velocity = Vector2(math.sin(time.time() * 3) * 100, self.speed)
        elif self.type == EnemyType.BOSS:
            # Boss movement pattern
            self.velocity = Vector2(math.sin(time.time() * 2) * 50, 20)

class PowerUp(GameObject):
    def __init__(self, pos: Vector2, power_type: str):
        super().__init__(pos, 12, '#00ffff')
        self.power_type = power_type
        self.lifetime = 10.0  # 10 seconds
        
    def update(self, dt: float):
        super().update(dt)
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False

class Particle:
    def __init__(self, pos: Vector2, velocity: Vector2, color: str, lifetime: float):
        self.pos = pos
        self.velocity = velocity
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.uniform(2, 6)
        
    def update(self, dt: float):
        self.pos = self.pos + self.velocity * dt
        self.lifetime -= dt
        
    def is_alive(self) -> bool:
        return self.lifetime > 0

class SpaceShooter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Space Shooter")
        self.root.geometry("800x600")
        self.root.configure(bg='#000011')
        self.root.resizable(False, False)
        
        # Game constants
        self.WIDTH = 800
        self.HEIGHT = 600
        
        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.level = 1
        self.lives = 3
        self.wave = 1
        self.high_scores = self.load_high_scores()
        
        # Game objects
        self.player = Player(Vector2(self.WIDTH // 2, self.HEIGHT - 50))
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.power_ups = []
        self.particles = []
        
        # Timing
        self.last_time = time.time()
        self.enemy_spawn_timer = 0
        self.wave_timer = 0
        self.boss_spawned = False
        
        # Input handling
        self.keys_pressed = set()
        
        self.setup_ui()
        self.bind_events()
        
    def setup_ui(self):
        """Initialize the user interface"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#000011')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Menu frame
        self.menu_frame = tk.Frame(self.main_frame, bg='#000011')
        
        # Game frame
        self.game_frame = tk.Frame(self.main_frame, bg='#000011')
        
        # Canvas for game
        self.canvas = tk.Canvas(
            self.game_frame,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg='#000011',
            highlightthickness=0
        )
        
        # UI frame for score, lives, etc.
        self.ui_frame = tk.Frame(self.game_frame, bg='#000011')
        
        self.setup_menu()
        self.setup_game_ui()
        self.show_menu()
        
    def setup_menu(self):
        """Setup the main menu"""
        title = tk.Label(
            self.menu_frame,
            text="SPACE SHOOTER",
            font=("Arial", 36, "bold"),
            fg='#00ffff',
            bg='#000011'
        )
        title.pack(pady=80)
        
        subtitle = tk.Label(
            self.menu_frame,
            text="Defend Earth from the alien invasion!",
            font=("Arial", 16),
            fg='#ffffff',
            bg='#000011'
        )
        subtitle.pack(pady=20)
        
        controls = tk.Label(
            self.menu_frame,
            text="Controls: WASD/Arrows to move, SPACE to shoot",
            font=("Arial", 12),
            fg='#cccccc',
            bg='#000011'
        )
        controls.pack(pady=10)
        
        # Menu buttons
        button_style = {
            'font': ("Arial", 14, "bold"),
            'fg': '#ffffff',
            'bg': '#333366',
            'activeforeground': '#ffffff',
            'activebackground': '#4444aa',
            'relief': 'flat',
            'bd': 0,
            'pady': 12,
            'padx': 40
        }
        
        start_btn = tk.Button(
            self.menu_frame,
            text="START MISSION",
            command=self.start_game,
            **button_style
        )
        start_btn.pack(pady=15)
        
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
        
    def setup_game_ui(self):
        """Setup game UI elements"""
        self.score_label = tk.Label(
            self.ui_frame,
            text="Score: 0",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#000011'
        )
        
        self.lives_label = tk.Label(
            self.ui_frame,
            text="Lives: 3",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#000011'
        )
        
        self.level_label = tk.Label(
            self.ui_frame,
            text="Level: 1",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#000011'
        )
        
        self.wave_label = tk.Label(
            self.ui_frame,
            text="Wave: 1",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#000011'
        )
        
    def bind_events(self):
        """Bind keyboard events"""
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        self.root.focus_set()
        
    def on_key_press(self, event):
        """Handle key press events"""
        self.keys_pressed.add(event.keysym.lower())
        
        if self.state == GameState.PLAYING:
            if event.keysym.lower() == 'space':
                self.player_shoot()
            elif event.keysym.lower() == 'p':
                self.toggle_pause()
        elif self.state == GameState.PAUSED:
            if event.keysym.lower() == 'p':
                self.toggle_pause()
        elif self.state == GameState.GAME_OVER:
            if event.keysym.lower() == 'r':
                self.start_game()
            elif event.keysym.lower() == 'escape':
                self.show_menu()
                
    def on_key_release(self, event):
        """Handle key release events"""
        self.keys_pressed.discard(event.keysym.lower())
        
    def start_game(self):
        """Initialize and start a new game"""
        self.state = GameState.PLAYING
        self.score = 0
        self.level = 1
        self.lives = 3
        self.wave = 1
        self.boss_spawned = False
        
        # Reset player
        self.player = Player(Vector2(self.WIDTH // 2, self.HEIGHT - 50))
        
        # Clear all game objects
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.power_ups = []
        self.particles = []
        
        # Reset timers
        self.enemy_spawn_timer = 0
        self.wave_timer = 0
        self.last_time = time.time()
        
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
        
        # Pack UI elements
        self.ui_frame.pack(fill=tk.X, pady=5)
        self.score_label.pack(side=tk.LEFT, padx=20)
        self.lives_label.pack(side=tk.LEFT, padx=20)
        self.level_label.pack(side=tk.LEFT, padx=20)
        self.wave_label.pack(side=tk.LEFT, padx=20)
        self.canvas.pack()
        
    def show_high_scores(self):
        """Display high scores window"""
        scores_window = tk.Toplevel(self.root)
        scores_window.title("High Scores")
        scores_window.geometry("350x450")
        scores_window.configure(bg='#000011')
        scores_window.resizable(False, False)
        
        title = tk.Label(
            scores_window,
            text="GALACTIC HEROES",
            font=("Arial", 20, "bold"),
            fg='#00ffff',
            bg='#000011'
        )
        title.pack(pady=20)
        
        for i, score in enumerate(self.high_scores[:10], 1):
            score_text = f"{i:2d}. {score:8d} pts"
            score_label = tk.Label(
                scores_window,
                text=score_text,
                font=("Courier", 14),
                fg='#ffffff',
                bg='#000011'
            )
            score_label.pack(pady=3)
            
    def handle_input(self, dt: float):
        """Handle continuous input"""
        if self.state != GameState.PLAYING:
            return
            
        # Player movement
        move_speed = self.player.speed * dt
        
        if 'w' in self.keys_pressed or 'up' in self.keys_pressed:
            self.player.pos.y = max(0, self.player.pos.y - move_speed)
        if 's' in self.keys_pressed or 'down' in self.keys_pressed:
            self.player.pos.y = min(self.HEIGHT - self.player.size, self.player.pos.y + move_speed)
        if 'a' in self.keys_pressed or 'left' in self.keys_pressed:
            self.player.pos.x = max(0, self.player.pos.x - move_speed)
        if 'd' in self.keys_pressed or 'right' in self.keys_pressed:
            self.player.pos.x = min(self.WIDTH - self.player.size, self.player.pos.x + move_speed)
            
    def player_shoot(self):
        """Player shoots bullets"""
        if self.player.shoot_cooldown <= 0:
            # Multiple bullets based on power level
            if self.player.power_level == 1:
                bullet = Bullet(
                    Vector2(self.player.pos.x, self.player.pos.y - 10),
                    Vector2(0, -500)
                )
                self.bullets.append(bullet)
            elif self.player.power_level == 2:
                # Double shot
                for offset in [-8, 8]:
                    bullet = Bullet(
                        Vector2(self.player.pos.x + offset, self.player.pos.y - 10),
                        Vector2(0, -500)
                    )
                    self.bullets.append(bullet)
            elif self.player.power_level >= 3:
                # Triple shot
                for angle in [-0.3, 0, 0.3]:
                    bullet = Bullet(
                        Vector2(self.player.pos.x, self.player.pos.y - 10),
                        Vector2(math.sin(angle) * 500, -math.cos(angle) * 500)
                    )
                    self.bullets.append(bullet)
                    
            self.player.shoot_cooldown = 0.15
            self.play_sound('shoot')
            
    def spawn_enemies(self, dt: float):
        """Spawn enemies based on level and wave"""
        if self.state != GameState.PLAYING:
            return
            
        self.enemy_spawn_timer += dt
        self.wave_timer += dt
        
        # Check for boss spawn
        if self.wave_timer > 30 and not self.boss_spawned and len(self.enemies) == 0:
            self.spawn_boss()
            return
            
        # Regular enemy spawning
        spawn_rate = max(0.5, 2.0 - self.level * 0.1)
        if self.enemy_spawn_timer > spawn_rate:
            self.enemy_spawn_timer = 0
            
            # Choose enemy type based on level
            enemy_types = [EnemyType.BASIC]
            if self.level >= 2:
                enemy_types.append(EnemyType.FAST)
            if self.level >= 3:
                enemy_types.append(EnemyType.HEAVY)
            if self.level >= 4:
                enemy_types.append(EnemyType.BOMBER)
                
            enemy_type = random.choice(enemy_types)
            x = random.randint(20, self.WIDTH - 20)
            enemy = Enemy(Vector2(x, -20), enemy_type)
            self.enemies.append(enemy)
            
    def spawn_boss(self):
        """Spawn a boss enemy"""
        boss = Enemy(Vector2(self.WIDTH // 2, -60), EnemyType.BOSS)
        self.enemies.append(boss)
        self.boss_spawned = True
        self.state = GameState.BOSS_BATTLE
        
    def enemy_shoot(self, enemy: Enemy):
        """Enemy shoots at player"""
        if enemy.shoot_cooldown <= 0:
            # Calculate direction to player
            dx = self.player.pos.x - enemy.pos.x
            dy = self.player.pos.y - enemy.pos.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                speed = 200
                velocity = Vector2(dx/distance * speed, dy/distance * speed)
                bullet = Bullet(enemy.pos, velocity, '#ff4444')
                self.enemy_bullets.append(bullet)
                
            if enemy.type == EnemyType.BOSS:
                enemy.shoot_cooldown = 0.5
            elif enemy.type == EnemyType.BOMBER:
                enemy.shoot_cooldown = 1.0
            else:
                enemy.shoot_cooldown = 2.0
                
    def spawn_power_up(self, pos: Vector2):
        """Spawn a power-up at the given position"""
        if random.random() < 0.3:  # 30% chance
            power_types = ['health', 'power', 'shield', 'rapid_fire']
            power_type = random.choice(power_types)
            power_up = PowerUp(pos, power_type)
            self.power_ups.append(power_up)
            
    def apply_power_up(self, power_type: str):
        """Apply power-up effect to player"""
        if power_type == 'health':
            self.player.health = min(self.player.max_health, self.player.health + 25)
        elif power_type == 'power':
            self.player.power_level = min(3, self.player.power_level + 1)
        elif power_type == 'shield':
            self.player.shield = 5.0
        elif power_type == 'rapid_fire':
            self.player.shoot_cooldown = -2.0  # Negative for rapid fire
            
        self.play_sound('powerup')
        
    def create_explosion(self, pos: Vector2, color: str = '#ffaa00'):
        """Create explosion particle effect"""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            velocity = Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            
            particle = Particle(
                Vector2(pos.x, pos.y),
                velocity,
                color,
                random.uniform(0.5, 1.5)
            )
            self.particles.append(particle)
            
    def update_game(self, dt: float):
        """Update all game objects"""
        if self.state != GameState.PLAYING and self.state != GameState.BOSS_BATTLE:
            return
            
        # Update player
        self.player.update(dt)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.pos.y < 0 or bullet.pos.y > self.HEIGHT:
                self.bullets.remove(bullet)
                
        for bullet in self.enemy_bullets[:]:
            bullet.update(dt)
            if bullet.pos.y < 0 or bullet.pos.y > self.HEIGHT:
                self.enemy_bullets.remove(bullet)
                
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt, self.player.pos)
            
            # Enemy shooting
            if random.random() < 0.01:  # 1% chance per frame
                self.enemy_shoot(enemy)
                
            # Remove enemies that are off screen
            if enemy.pos.y > self.HEIGHT + 50:
                self.enemies.remove(enemy)
                
        # Update power-ups
        for power_up in self.power_ups[:]:
            power_up.update(dt)
            if not power_up.active:
                self.power_ups.remove(power_up)
                
        # Update particles
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.is_alive():
                self.particles.remove(particle)
                
        # Check collisions
        self.check_collisions()
        
        # Spawn enemies
        self.spawn_enemies(dt)
        
        # Check wave completion
        if self.boss_spawned and len(self.enemies) == 0:
            self.next_wave()
            
    def check_collisions(self):
        """Check all collision interactions"""
        # Player bullets vs enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.collides_with(enemy):
                    self.bullets.remove(bullet)
                    enemy.health -= bullet.damage
                    
                    if enemy.health <= 0:
                        self.score += enemy.points * self.level
                        self.create_explosion(enemy.pos)
                        self.spawn_power_up(enemy.pos)
                        self.enemies.remove(enemy)
                        self.play_sound('explosion')
                    break
                    
        # Enemy bullets vs player
        for bullet in self.enemy_bullets[:]:
            if bullet.collides_with(self.player):
                self.enemy_bullets.remove(bullet)
                if self.player.shield <= 0:
                    self.player.health -= 10
                    self.create_explosion(self.player.pos, '#ff0000')
                    if self.player.health <= 0:
                        self.player_death()
                        
        # Enemies vs player
        for enemy in self.enemies[:]:
            if enemy.collides_with(self.player):
                if self.player.shield <= 0:
                    self.player.health -= 20
                    self.create_explosion(self.player.pos, '#ff0000')
                    if self.player.health <= 0:
                        self.player_death()
                enemy.health = 0  # Enemy also dies
                
        # Player vs power-ups
        for power_up in self.power_ups[:]:
            if power_up.collides_with(self.player):
                self.apply_power_up(power_up.power_type)
                self.power_ups.remove(power_up)
                
    def player_death(self):
        """Handle player death"""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over()
        else:
            # Respawn player
            self.player.health = self.player.max_health
            self.player.pos = Vector2(self.WIDTH // 2, self.HEIGHT - 50)
            self.player.shield = 3.0  # Temporary invincibility
            
    def next_wave(self):
        """Progress to next wave"""
        self.wave += 1
        self.boss_spawned = False
        self.wave_timer = 0
        
        if self.wave % 3 == 0:  # Every 3 waves = new level
            self.level += 1
            
        # Bonus for completing wave
        self.score += 100 * self.level
        
    def toggle_pause(self):
        """Toggle game pause"""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            self.last_time = time.time()
            self.game_loop()
            
    def game_over(self):
        """Handle game over"""
        self.state = GameState.GAME_OVER
        self.update_high_scores()
        
    def update_high_scores(self):
        """Update high scores"""
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:10]
        self.save_high_scores()
        
    def load_high_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists('space_shooter_scores.json'):
                with open('space_shooter_scores.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return [0] * 10
        
    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open('space_shooter_scores.json', 'w') as f:
                json.dump(self.high_scores, f)
        except:
            pass
            
    def play_sound(self, sound_type: str):
        """Play sound effects using system bell"""
        try:
            if sound_type == 'shoot':
                self.root.bell()
            elif sound_type == 'explosion':
                for _ in range(2):
                    self.root.bell()
            elif sound_type == 'powerup':
                for _ in range(3):
                    self.root.bell()
        except:
            pass
            
    def draw_starfield(self):
        """Draw animated starfield background"""
        self.canvas.delete("star")
        
        # Create moving stars
        for _ in range(50):
            x = random.randint(0, self.WIDTH)
            y = (random.randint(0, self.HEIGHT) + time.time() * 30) % self.HEIGHT
            brightness = random.choice(['#444444', '#666666', '#888888', '#aaaaaa'])
            
            self.canvas.create_oval(
                x, y, x + 2, y + 2,
                fill=brightness, outline='', tags="star"
            )
            
    def draw_player(self):
        """Draw the player ship"""
        self.canvas.delete("player")
        
        x, y = self.player.pos.x, self.player.pos.y
        size = self.player.size
        
        # Shield effect
        if self.player.shield > 0:
            shield_color = '#00ffff' if int(self.player.shield * 10) % 2 else '#0088ff'
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                outline=shield_color, width=3, tags="player"
            )
            
        # Player ship (triangle)
        points = [
            x, y - size//2,  # Top
            x - size//2, y + size//2,  # Bottom left
            x + size//2, y + size//2   # Bottom right
        ]
        
        color = self.player.color
        if self.player.health < 30:
            color = '#ffaa00'  # Orange when low health
            
        self.canvas.create_polygon(
            points, fill=color, outline='#ffffff', width=2, tags="player"
        )
        
        # Health bar
        bar_width = 60
        bar_height = 8
        health_ratio = self.player.health / self.player.max_health
        
        self.canvas.create_rectangle(
            x - bar_width//2, y + size + 5,
            x + bar_width//2, y + size + 5 + bar_height,
            fill='#333333', outline='#666666', tags="player"
        )
        
        health_color = '#00ff00' if health_ratio > 0.5 else '#ffaa00' if health_ratio > 0.25 else '#ff0000'
        self.canvas.create_rectangle(
            x - bar_width//2, y + size + 5,
            x - bar_width//2 + bar_width * health_ratio, y + size + 5 + bar_height,
            fill=health_color, outline='', tags="player"
        )
        
    def draw_bullets(self):
        """Draw all bullets"""
        self.canvas.delete("bullet")
        
        # Player bullets
        for bullet in self.bullets:
            x, y = bullet.pos.x, bullet.pos.y
            self.canvas.create_oval(
                x - bullet.size, y - bullet.size,
                x + bullet.size, y + bullet.size,
                fill=bullet.color, outline='#ffffff', tags="bullet"
            )
            
        # Enemy bullets
        for bullet in self.enemy_bullets:
            x, y = bullet.pos.x, bullet.pos.y
            self.canvas.create_oval(
                x - bullet.size, y - bullet.size,
                x + bullet.size, y + bullet.size,
                fill=bullet.color, outline='#aa0000', tags="bullet"
            )
            
    def draw_enemies(self):
        """Draw all enemies"""
        self.canvas.delete("enemy")
        
        for enemy in self.enemies:
            x, y = enemy.pos.x, enemy.pos.y
            size = enemy.size
            
            if enemy.type == EnemyType.BOSS:
                # Boss design
                self.canvas.create_rectangle(
                    x - size, y - size//2,
                    x + size, y + size//2,
                    fill=enemy.color, outline='#ffffff', width=2, tags="enemy"
                )
                
                # Boss health bar
                bar_width = 100
                health_ratio = enemy.health / 50
                self.canvas.create_rectangle(
                    x - bar_width//2, y - size - 15,
                    x + bar_width//2, y - size - 5,
                    fill='#333333', outline='#666666', tags="enemy"
                )
                self.canvas.create_rectangle(
                    x - bar_width//2, y - size - 15,
                    x - bar_width//2 + bar_width * health_ratio, y - size - 5,
                    fill='#ff0000', outline='', tags="enemy"
                )
            else:
                # Regular enemy design
                if enemy.type == EnemyType.BASIC:
                    # Square
                    self.canvas.create_rectangle(
                        x - size//2, y - size//2,
                        x + size//2, y + size//2,
                        fill=enemy.color, outline='#ffffff', tags="enemy"
                    )
                elif enemy.type == EnemyType.FAST:
                    # Diamond
                    points = [
                        x, y - size//2,
                        x + size//2, y,
                        x, y + size//2,
                        x - size//2, y
                    ]
                    self.canvas.create_polygon(
                        points, fill=enemy.color, outline='#ffffff', tags="enemy"
                    )
                elif enemy.type == EnemyType.HEAVY:
                    # Hexagon
                    points = []
                    for i in range(6):
                        angle = i * math.pi / 3
                        px = x + math.cos(angle) * size//2
                        py = y + math.sin(angle) * size//2
                        points.extend([px, py])
                    self.canvas.create_polygon(
                        points, fill=enemy.color, outline='#ffffff', tags="enemy"
                    )
                elif enemy.type == EnemyType.BOMBER:
                    # Circle
                    self.canvas.create_oval(
                        x - size//2, y - size//2,
                        x + size//2, y + size//2,
                        fill=enemy.color, outline='#ffffff', tags="enemy"
                    )
                    
    def draw_power_ups(self):
        """Draw power-ups"""
        self.canvas.delete("powerup")
        
        for power_up in self.power_ups:
            x, y = power_up.pos.x, power_up.pos.y
            size = power_up.size
            
            # Rotating effect
            rotation = time.time() * 5
            points = []
            for i in range(4):
                angle = i * math.pi / 2 + rotation
                px = x + math.cos(angle) * size
                py = y + math.sin(angle) * size
                points.extend([px, py])
                
            self.canvas.create_polygon(
                points, fill=power_up.color, outline='#ffffff', width=2, tags="powerup"
            )
            
            # Power-up type indicator
            text = power_up.power_type[0].upper()
            self.canvas.create_text(
                x, y, text=text, font=("Arial", 8, "bold"),
                fill='#000000', tags="powerup"
            )
            
    def draw_particles(self):
        """Draw particle effects"""
        self.canvas.delete("particle")
        
        for particle in self.particles:
            alpha = particle.lifetime / particle.max_lifetime
            x, y = particle.pos.x, particle.pos.y
            
            self.canvas.create_oval(
                x - particle.size * alpha, y - particle.size * alpha,
                x + particle.size * alpha, y + particle.size * alpha,
                fill=particle.color, outline='', tags="particle"
            )
            
    def draw_ui_overlay(self):
        """Draw UI overlays"""
        self.canvas.delete("ui_overlay")
        
        # Update UI labels
        self.score_label.config(text=f"Score: {self.score}")
        self.lives_label.config(text=f"Lives: {self.lives}")
        self.level_label.config(text=f"Level: {self.level}")
        self.wave_label.config(text=f"Wave: {self.wave}")
        
        # Pause indicator
        if self.state == GameState.PAUSED:
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2,
                text="PAUSED\nPress 'P' to continue",
                font=("Arial", 24, "bold"),
                fill='#ffff00',
                justify=tk.CENTER,
                tags="ui_overlay"
            )
            
        # Boss battle indicator
        if self.state == GameState.BOSS_BATTLE:
            self.canvas.create_text(
                self.WIDTH // 2, 50,
                text="BOSS BATTLE!",
                font=("Arial", 20, "bold"),
                fill='#ff0000',
                tags="ui_overlay"
            )
            
        # Game over screen
        if self.state == GameState.GAME_OVER:
            self.canvas.create_rectangle(
                0, 0, self.WIDTH, self.HEIGHT,
                fill='#000000', stipple='gray25', tags="ui_overlay"
            )
            
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 - 80,
                text="MISSION FAILED",
                font=("Arial", 32, "bold"),
                fill='#ff0000',
                tags="ui_overlay"
            )
            
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 - 30,
                text=f"Final Score: {self.score}",
                font=("Arial", 18, "bold"),
                fill='#ffffff',
                tags="ui_overlay"
            )
            
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 + 10,
                text=f"Waves Survived: {self.wave}",
                font=("Arial", 16),
                fill='#ffffff',
                tags="ui_overlay"
            )
            
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 + 50,
                text="Press 'R' to restart or 'ESC' for menu",
                font=("Arial", 14),
                fill='#cccccc',
                tags="ui_overlay"
            )
            
    def draw_game(self):
        """Draw all game elements"""
        self.canvas.delete("all")
        self.draw_starfield()
        self.draw_particles()
        self.draw_power_ups()
        self.draw_enemies()
        self.draw_bullets()
        self.draw_player()
        self.draw_ui_overlay()
        
    def game_loop(self):
        """Main game loop"""
        if self.state in [GameState.PLAYING, GameState.BOSS_BATTLE]:
            current_time = time.time()
            dt = current_time - self.last_time
            self.last_time = current_time
            
            # Cap delta time to prevent large jumps
            dt = min(dt, 1/30)  # Max 30 FPS equivalent
            
            self.handle_input(dt)
            self.update_game(dt)
            self.draw_game()
            
            # Continue loop
            self.root.after(16, self.game_loop)  # ~60 FPS
        elif self.state == GameState.PAUSED:
            self.draw_ui_overlay()
            
    def run(self):
        """Start the game application"""
        print("🚀 Advanced Space Shooter Starting...")
        print("\nFeatures:")
        print("  • Multiple enemy types with unique behaviors")
        print("  • Boss battles every 3 waves")
        print("  • Power-up system (Health, Weapons, Shield)")
        print("  • Particle effects and explosions")
        print("  • Progressive difficulty scaling")
        print("  • High score tracking")
        print("  • Smooth 60 FPS gameplay")
        print("\nControls:")
        print("  • WASD or Arrow Keys to move")
        print("  • SPACE to shoot")
        print("  • P to pause/unpause")
        print("  • R to restart (when game over)")
        print("  • ESC to return to menu")
        print("\nDefend Earth from the alien invasion!")
        
        self.root.mainloop()

def main():
    """Main function to run the space shooter"""
    try:
        game = SpaceShooter()
        game.run()
    except KeyboardInterrupt:
        print("\n👋 Thanks for defending Earth!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()