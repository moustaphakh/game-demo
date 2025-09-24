# imports
import pygame
from pathlib import Path
from tiles import load_level, find_char, iter_tiles, build_solids
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR, TILE_SIZE,
    WALL_COLOR, COIN_COLOR, FLAG_COLOR
)
from player import Player

# Absolute path to levels/level1.txt
LEVEL_PATH = Path(__file__).resolve().parent.parent / "levels" / "level1.txt"

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Demo")
    clock = pygame.time.Clock()

    # load level
    rows = load_level(LEVEL_PATH)
    solids = build_solids(rows, '#', TILE_SIZE)

    # find player spawn and create Player
    spawn = find_char(rows, "P") or (1, 1)   # fallback so it won't crash if P missing
    px = spawn[0] * TILE_SIZE
    py = spawn[1] * TILE_SIZE
    player = Player(px, py)

    running = True
    while running:
        # get dt and events
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # input + update
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update(dt, solids)

        # draw everything
        screen.fill(BG_COLOR)
        for tx, ty, ch in iter_tiles(rows):
            x = tx * TILE_SIZE
            y = ty * TILE_SIZE
            if ch == '#':
                pygame.draw.rect(screen, WALL_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
            elif ch == 'C':
                pygame.draw.circle(screen, COIN_COLOR, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 3)
            elif ch == 'F':
                pygame.draw.rect(screen, FLAG_COLOR, (x + TILE_SIZE // 4, y, TILE_SIZE // 2, TILE_SIZE))

        player.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
