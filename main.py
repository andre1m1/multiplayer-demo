import pygame
import sys
from common import *
from common import PlayerCommon

pygame.init()

class Player(PlayerCommon):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.rect = pygame.Rect(self.x, self.y, 60, 60)

    def draw_self(self, screen : pygame.Surface):
        pygame.draw.rect(screen, RED, self.rect)


def main() -> None:
    
    screen : pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock : pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Multiplayer Demo")
    p = Player(10, 10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Exit Succesfully")
                sys.exit(0)

        screen.fill(BLACK)
        p.draw_self(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

