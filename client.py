import pygame
import sys
import socket
import json
from common import *

pygame.init()

class Player(PlayerCommon):
    def __init__(self, x, y, conn) -> None:
        super().__init__(x, y, conn)
        self.rect = pygame.Rect(self.x, self.y, 60, 60)

    def draw_self(self, screen : pygame.Surface):
        pygame.draw.rect(screen, RED, self.rect)


def main() -> None:
    screen : pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock : pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Multiplayer Demo")
    
    conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_socket.connect((HOST, PORT))
    p = Player(10, 10, conn_socket)

    try:
        mess = json.loads(p.conn.recv(1024))
        if mess["type"] == "hello":
            p.conn.sendall(json.dumps(mess).encode("utf-8"))
        print(mess)
    
    except Exception as e:
        print(e)
        p.conn.close()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                p.conn.close()
                pygame.quit()
                print("Exit Succesfully")
                sys.exit(0)

        screen.fill(BLACK)
        p.draw_self(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

