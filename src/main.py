#imports
import pygame
from pathlib import Path #for file paths
from config import *
from tiles import load_level, find_char
#this is the main code

# Absolute path to levels/level1.txt no matter where you run from:
LEVEL_PATH = Path(__file__).resolve().parent.parent / "levels" / "level1.txt"

def main():
    #initialization

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Demo")
    clock = pygame.time.Clock()
    #load level
    rows = load_level(LEVEL_PATH)
    print(rows)
    w, h = len(rows[0]), len(rows)
    #print some info about the level
    print(f"Level size: {w} x {h} tiles")
    print(f"Level size: {w * TILE_SIZE} x {h * TILE_SIZE} pixels")
    print("Level layout:")
    for row in rows:
        print(" ".join(row))
        print()

    #find player spawn
    spawn = find_char(rows, "P")
    if spawn:
        px = spawn[0] * TILE_SIZE
        py = spawn[1] * TILE_SIZE
        print(f"Player spawn tile: {spawn} -> pixels: ({px}, {py})")
    else:
        print("No player spawn (P) found")

    running = True
    while running:
        #for quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        screen.fill(BG_COLOR)

        #display update
        pygame.display.flip()

        #framerate
        clock.tick(FPS)

    pygame.quit()
#entry point
if __name__ == "__main__":
    main()
