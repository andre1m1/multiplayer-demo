import socket
from enum import Enum, auto
from typing import Optional

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
MOVE_SPEED = 20

type Move = dict[str , int]
type Err = Exception | None


class Player:
    def __init__(self, x : int, y : int, id : int, conn : Optional[socket.socket]) -> None:
        self.x = x
        self.y = y
        self.id = id
        self.conn = conn
    
    def __str__(self) -> str:
        return f"X: {self.x}, Y: {self.y}, Connection: {self.conn}"

    
    def __repr__(self) -> str:
        return f"Player(X: {self.x}, Y: {self.y}, Connection: {self.conn})"


class MessageType(Enum):
    HELLO         = auto()
    INIT          = auto()
    PLAYER_JOINED = auto()
    PLAYER_LEFT   = auto()
    PLAYER_MOVE   = auto()

