# This file contains the player details
import pygame
from config import PLAYER_SPEED, JUMP_VELOCITY, GRAVITY, MAX_FALL_SPEED, TILE_SIZE, PLAYER_COLOR, MAX_JUMPS
# NEW imports for variable jump
from config import LOW_JUMP_GRAVITY, FALL_GRAVITY, MAX_JUMP_HOLD_MS, JUMP_CUT_MULTIPLIER

class Player:
    def __init__(self, px, py):
        # Initialize player rectangle and physics variables
        self.rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
        self.vx = 0.0  # Horizontal velocity
        self.vy = 0.0  # Vertical velocity
        self.prev_vy = 0.0  # Track last frame's vy (for apex detection)
        self.on_ground = False  # Is the player standing on the ground?

        # Debug helpers for measuring jump height
        self._jump_start_y = None  # set when a jump starts

        # Double-jump state
        self.max_jumps = MAX_JUMPS
        self.jumps_left = MAX_JUMPS
        self._jump_was_down = False  # edge detection so holding doesn't spam jumps

        # --- Variable-jump state (new) ---
        self._jump_held = False
        self._jump_hold_ms = 0.0

    def handle_input(self, keys):
        # keyboard input for movement and jumping
        self.vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED  # Move left
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED   # Move right

        # Jump if on ground and jump key is pressed -> (buffer/coyote later)
        jump_down = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
        if jump_down and not self._jump_was_down:
            self._try_jump()

        # Jump cut: releasing jump early trims upward speed for short hops
        if (not jump_down) and self._jump_was_down:
            if self.vy < 0:
                self.vy *= JUMP_CUT_MULTIPLIER

        # track hold state
        self._jump_held = jump_down
        self._jump_was_down = jump_down

    # double jump logic
    def _try_jump(self):
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False
            self.jumps_left = self.max_jumps - 1  # leave air jumps available
            self._jump_start_y = self.rect.y
            self._jump_hold_ms = 0.0
        elif self.jumps_left > 0:
            self.vy = JUMP_VELOCITY
            self.jumps_left -= 1
            if self._jump_start_y is None:
                self._jump_start_y = self.rect.y
            self._jump_hold_ms = 0.0

    def apply_gravity(self, dt):
        # Apply gravity to vertical velocity, capped at max fall speed
        self.vy = min(self.vy + GRAVITY * dt, MAX_FALL_SPEED)

    def move_and_collide(self, dx, dy, solids):
        # Move horizontally and check for collisions
        self.rect.x += int(dx)
        for s in solids:
            if self.rect.colliderect(s):
                if dx > 0:   # Moving right; hit the left side of a solid
                    self.rect.right = s.left
                elif dx < 0: # Moving left; hit the right side of a solid
                    self.rect.left = s.right

        # Move vertically and check for collisions
        self.rect.y += int(dy)
        was_on_ground = self.on_ground
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

        # Reset jumps when landing this frame
        if not was_on_ground and self.on_ground:
            self.jumps_left = self.max_jumps
            self._jump_start_y = None  # end of jump sequence
            self._jump_hold_ms = 0.0   # reset hold timer on landing

    def update(self, dt, solids):
        # remember last-frame vy
        self.prev_vy = self.vy

    
        # Variable jump gravity logic
        if self.vy < 0:  # going up
            if self._jump_held and self._jump_hold_ms < MAX_JUMP_HOLD_MS:
                g = LOW_JUMP_GRAVITY      # gentler while holding
            else:
                g = GRAVITY               # normal once hold window ends
        else:              # going down
            g = FALL_GRAVITY              # snappier fall

        # Apply chosen gravity (capped)
        self.vy = min(self.vy + g * dt, MAX_FALL_SPEED)

        # Track how long jump is held (only while rising)
        if self.vy < 0 and self._jump_held:
            self._jump_hold_ms += dt * 1000.0

        self.move_and_collide(self.vx * dt, self.vy * dt, solids)

        # detect apex of jump for debugging
        if self.prev_vy < 0 <= self.vy and self._jump_start_y is not None:
            rise = self._jump_start_y - self.rect.y
            print(f"Apex reached. Measured jump height: {rise:.1f}px  (~{rise/TILE_SIZE:.2f} tiles)")
            self._jump_start_y = None  # reset until next jump

    def draw(self, surface):
        # Draw the player rectangle on the given surface
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)
