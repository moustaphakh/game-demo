# imports
from tiles import (
    load_level, find_char, iter_tiles, build_solids,
    build_coins, build_flag
)

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR, TILE_SIZE,
    WALL_COLOR, COIN_COLOR, FLAG_COLOR, PLAYER_COLOR,
    WALL_CHAR, COIN_CHAR, FLAG_CHAR, PLAYER_CHAR, LEVELS
)
from player import Player
import pygame
from pathlib import Path

def load_world(level_path):
    """Load one level's world data (rows, solids, coins, flag, spawn px/py)."""
    rows   = load_level(level_path)
    solids = build_solids(rows, '#', TILE_SIZE)
    coins  = build_coins(rows, 'C', TILE_SIZE)
    flag   = build_flag(rows, 'F', TILE_SIZE)
    sx, sy = find_char(rows, 'P') or (1, 1)
    return rows, solids, coins, flag, (sx * TILE_SIZE, sy * TILE_SIZE)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Demo")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    # load level 0
    level_path = 0  # Change index to load different levels
    rows, solids, coins, flag, (spawn_x, spawn_y) = load_world(LEVELS[level_path])
    print(f"Loaded level from {level_path}, size: {len(rows[0])}x{len(rows)} tiles")
    print(f"Player spawn at: {spawn_x}, {spawn_y}")


    # player setup
    sx, sy = find_char(rows, PLAYER_CHAR) or (1, 1)
    player = Player(sx*TILE_SIZE, sy*TILE_SIZE)
    
    score = 0
    running = True
    while running:
        # get dt and events
        dt = clock.tick(FPS) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # input + update
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update(dt, solids)

        # coin pickup (check collision with player)
        for c in coins[:]:
            if player.rect.colliderect(c):
                coins.remove(c)
                score += 1

        # reach flag -> go to next level
        if flag and player.rect.colliderect(flag):
            level_path += 1
            if level_path < len(LEVELS):
                rows, solids, coins, flag, (px, py) = load_world(LEVELS[level_path])
                player = Player(px, py)
            else:
                # all levels done
                print("All levels complete! Congrats!")
                running = False

        # draw
        screen.fill(BG_COLOR)
        # walls from ASCII
        for tx, ty, ch in iter_tiles(rows):
            if ch == WALL_CHAR:
                x, y = tx*TILE_SIZE, ty*TILE_SIZE
                pygame.draw.rect(screen, WALL_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
        # coins from list
        for c in coins:
            pygame.draw.circle(screen, COIN_COLOR,
                               (c.x + TILE_SIZE//2, c.y + TILE_SIZE//2),
                               TILE_SIZE//3)
        # flag
        if flag:
            pygame.draw.rect(screen, FLAG_COLOR,
                             (flag.x + TILE_SIZE//4, flag.y, TILE_SIZE//2, TILE_SIZE))
        # player
        player.draw(screen)
        # HUD
        hud = font.render(f"Score: {score}", True, (230,230,230))
        screen.blit(hud, (8, 8))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
#this is the main file that runs the game loop and initializes the game