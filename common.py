from socket import gethostbyname, gethostname


# Screen settings
WIDTH = 800
HEIGHT = 800

# Clock
FPS = 60

# Colors
BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)

RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# Game
HOST = gethostbyname(gethostname())
PORT = 9090


class PlayerCommon:
    def __init__(self, x, y, conn) -> None:
        self.x = x
        self.y = y
        self.conn = conn