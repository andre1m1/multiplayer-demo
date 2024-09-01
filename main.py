import pygame
import sys
from settings import *

pygame.init()


def main() -> None:
    
    screen : pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock : pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Multiplayer Demo")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Exit Succesfully")
                sys.exit(0)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

