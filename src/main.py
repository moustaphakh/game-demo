#imports
import pygame
#this is the main code
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR #importing constants from config.py

def main():
    #initialization
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Demo")
    clock = pygame.time.Clock()

    running = True
    while running:
        # Handle quit event
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
