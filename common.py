import socket
from enum import Enum, auto

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
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

class Player:
    def __init__(self, x, y, id, conn) -> None:
        self.x : int = x
        self.y : int = y
        self.id : int = id
        self.conn : socket.socket | None = conn


class MessageType(Enum):
    HELLO         = auto()
    INIT          = auto()
    PLAYER_JOINED = auto()
    PLAYER_LEFT   = auto()

