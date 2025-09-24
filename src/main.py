# imports
import pygame
from pathlib import Path
from tiles import load_level, find_char, iter_tiles, build_solids
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR, TILE_SIZE, WALL_COLOR, COIN_COLOR, FLAG_COLOR, PLAYER_COLOR

# Absolute path to levels/level1.txt
LEVEL_PATH = Path(__file__).resolve().parent.parent / "levels" / "level1.txt"


def main():
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Demo")
    clock = pygame.time.Clock()

    # load level
    rows = load_level(LEVEL_PATH)        
    solids = build_solids(rows, '#', TILE_SIZE)

    # find player spawn point   
    spawn = find_char(rows, "P")
    player_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    if spawn:
        player_rect.topleft = (spawn[0] * TILE_SIZE, spawn[1] * TILE_SIZE)
    # exit loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # draw tiles
        for tx, ty, ch in iter_tiles(rows):
            x = tx * TILE_SIZE
            y = ty * TILE_SIZE
            if ch == '#':
                pygame.draw.rect(screen, WALL_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
            elif ch == 'C':
                pygame.draw.circle(screen, COIN_COLOR, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 3)
            elif ch == 'F':
                pygame.draw.rect(screen, FLAG_COLOR, (x + TILE_SIZE // 4, y, TILE_SIZE // 2, TILE_SIZE))
  
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
