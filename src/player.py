# This file contains the player details
import pygame
from config import PLAYER_SPEED, JUMP_VELOCITY, GRAVITY, MAX_FALL_SPEED, TILE_SIZE

PLAYER_COLOR = (200, 140, 200)

class Player:
    def __init__(self, px, py):
        # Initialize player rectangle and physics variables
        self.rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
        self.vx = 0.0  # Horizontal velocity
        self.vy = 0.0  # Vertical velocity
        self.on_ground = False  # Is the player standing on the ground?

    def handle_input(self, keys):
        # keyboard input for movement and jumping
        self.vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED  # Move left
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED   # Move right
        # Jump if on ground and jump key is pressed -> will be upgraded to buffered jump later on
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False

    def apply_gravity(self, dt):
        # Apply gravity to vertical velocity, capped at max fall speed
        self.vy = min(self.vy + GRAVITY * dt, MAX_FALL_SPEED)

    def move_and_collide(self, dx, dy, solids):
        # Move horizontally and check for collisions
        self.rect.x += int(dx)
        for s in solids:
            if self.rect.colliderect(s):
                if dx > 0:  # Moving right; hit the left side of a solid
                    self.rect.right = s.left
                elif dx < 0:  # Moving left; hit the right side of a solid
                    self.rect.left  = s.right

        # Move vertically and check for collisions
        self.rect.y += int(dy)
        self.on_ground = False
        for s in solids:
            if self.rect.colliderect(s):
                if dy > 0:
                    # Falling; hit the top of a solid
                    self.rect.bottom = s.top
                    self.vy = 0
                    self.on_ground = True
                elif dy < 0:
                    # Jumping; hit the bottom of a solid
                    self.rect.top = s.bottom
                    self.vy = 0

    def update(self, dt, solids):
        # Update player physics and position
        self.apply_gravity(dt)
        self.move_and_collide(self.vx * dt, self.vy * dt, solids)

    def draw(self, surface):
        # Draw the player rectangle on the given surface
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)
