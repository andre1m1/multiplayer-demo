import pygame
import sys
import socket
import threading
import json
from common import *


pygame.init()

class ClientPlayer(Player):
    def __init__(self, x : int, y : int, id : int, conn = None) -> None:
        super().__init__(x, y, id, conn)
        self.rect = pygame.Rect(self.x, self.y, 60, 60)

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}, Connection: {self.conn}"

    def draw_self(self, screen : pygame.Surface) -> None:
        pygame.draw.rect(screen, RED, self.rect)


def connect_to_server() -> ClientPlayer:
    conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_socket.connect((HOST, PORT))
    try:
        msg : dict = json.loads(conn_socket.recv(1024))
        if msg["type"] != MessageType.HELLO.value:
            raise Exception("ERROR: Could not properly comunicate with server! ")
            
        conn_socket.sendall(json.dumps(msg).encode("utf-8"))

        msg = json.loads(conn_socket.recv(1024))
        if msg["type"] != MessageType.INIT.value:
            raise Exception("ERROR: Could not receive intial player data from server!")
        
        
        for p in msg["players"]:
            players_list.append(ClientPlayer(p["x"], p["y"], p["id"]))

        player = ClientPlayer(msg["x"], msg["y"], msg["id"], conn_socket)

    except Exception as e:
        print(e)
        conn_socket.close()
        sys.exit(1)

    return player


def handle_recv(conn) -> None:
    try:
        while True:
            msg : dict  = json.loads(conn.recv(1024))
            match msg["type"]:
                case MessageType.PLAYER_JOINED.value:
                    players_list.append(ClientPlayer(msg['x'], msg['y'], msg["id"]))
                
                case MessageType.PLAYER_LEFT.value:
                    for p in players_list:
                        if p.id == msg["id"]:
                            players_list.remove(p)

                case _:
                    raise Exception(f"Received unknown server message! : {msg}")

    except Exception as e:
        print(e)
        conn.close()
        sys.exit(1)


if __name__ == "__main__":
    screen : pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock : pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Multiplayer Demo")
    players_list: list[ClientPlayer] = []

    player = connect_to_server()
    player_thread = threading.Thread(target=handle_recv, args=(player.conn,))
    player_thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                player.conn.sendall(json.dumps({"type": MessageType.PLAYER_LEFT.value}).encode("utf-8"))
                player.conn.close()
                pygame.quit()
                print("Exit Succesfully")
                sys.exit(0)

        screen.fill(BLACK)
        player.draw_self(screen)

        for p in players_list:
            p.draw_self(screen)

        pygame.display.update()
        clock.tick(FPS)


