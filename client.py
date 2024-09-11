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

    def draw_self(self, screen : pygame.Surface) -> None:
        self.rect.x = self.x
        self.rect.y = self.y
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


def handle_recv(conn : socket.socket) -> None:
    try:
        while True:
            msg : dict  = json.loads(conn.recv(1024))
            match msg["type"]:
                case MessageType.PLAYER_JOINED.value:
                    print("Player Joined!")
                    players_list.append(ClientPlayer(msg['x'], msg['y'], msg["id"]))
                
                    continue
                case MessageType.PLAYER_LEFT.value:
                    for p in players_list:
                        if p.id == msg["id"]:
                            players_list.remove(p)
                            print("Player Left!")
                    continue

                case MessageType.PLAYER_MOVE.value:
                    for p in players_list:
                        if p.id == msg["id"]:
                            p.x, p.y = msg["pos"]

                    continue
                case _:
                    raise Exception(f"Received unknown server message! : {msg}")

    except Exception as e:
        print(e)
        conn.close()
        sys.exit(1)


def serialize_msg(msg: dict)-> bytes:
    return json.dumps(msg).encode("utf-8")

if __name__ == "__main__":
    screen : pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock : pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Multiplayer Demo")
    players_list: list[ClientPlayer] = []
    move_events : list[Move] = []
    player = connect_to_server()
    player_thread = threading.Thread(target=handle_recv, args=(player.conn,))
    player_thread.start()

    if player.conn is not None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    player.conn.sendall(serialize_msg({"type": MessageType.PLAYER_LEFT.value}))
                    player.conn.close()
                    player_thread.join()
                    pygame.quit()
                    print("Exit Succesfully")
                    sys.exit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player.y -= MOVE_SPEED
                        move_events.append({'y' : -MOVE_SPEED})
                    
                    elif event.key == pygame.K_s:
                        player.y += MOVE_SPEED
                        move_events.append({'y' : MOVE_SPEED})
                    
                    elif event.key == pygame.K_a:
                        player.x -= MOVE_SPEED
                        move_events.append({'x' : -MOVE_SPEED})
                    
                    elif event.key == pygame.K_d:
                        player.x += MOVE_SPEED
                        move_events.append({'x' : MOVE_SPEED})
                    
            if len(move_events) > 0:
                msg = {
                    "type" : MessageType.PLAYER_MOVE.value,
                    "moves": move_events
                }
                player.conn.sendall(serialize_msg(msg))
                move_events.clear()

            screen.fill(BLACK)
            player.draw_self(screen)

            for p in players_list:
                p.draw_self(screen)

            pygame.display.update()
            clock.tick(FPS)

    else:
        print("ERROR: Could not connect to the server!")
 
