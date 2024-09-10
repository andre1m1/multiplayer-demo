import socket
import threading
import random
import json
import logging
from common import *


type Err = Exception | None

class ServerPlayer(Player):
    def __init__(self, x : int, y : int, conn : socket.socket) -> None:
        super().__init__(x, y, conn)
        self.id = len(players_list) 


def close_conn(conn, addr, with_err: Err = None) -> None:
    conn.close()
    if with_err:
        logging.error(f"ERROR: {with_err} cause by client: {addr}")
        logging.error(f"Client {addr} disconnected!!!")
    else:
        logging.info(f"Client {addr} disconnected!")


def serialize_players(players_list : list[ServerPlayer]) -> list[dict]:
    players = []

    for player in players_list:
        players.append({
            "x" : player.x,
            "y" : player.y
        })

    return players


def handle_connection(client : socket.socket, addr : str) -> ServerPlayer | None:
    try:
        client.sendall(json.dumps({"type" : "hello"}).encode("utf-8"))

        hello_msg : dict = json.loads(client.recv(1024))

        if hello_msg["type"] != "hello":
            close_conn(client, addr)
            return None

        player = ServerPlayer(random.randrange(WIDTH), random.randrange(HEIGHT), client)
        players_list.append(player)

        player.conn.sendall(json.dumps({
            "type" : "init",
            "x": player.x,
            "y": player.y,
            "players" : serialize_players(players_list)
        }).encode("utf-8"))

        for p in players_list:
            p.conn.sendall(json.dumps({
                "type" : "player_joined",
                'x' : player.x,
                'y' : player.y
            }).encode("utf-8"))

        return player

    except Exception as e:
        close_conn(client, addr, e)
        players_list.remove(player)
        return None


def handle_client(client : socket.socket, addr : str) -> None:
    player = handle_connection(client, addr)
    
    if type(player) == ServerPlayer: 
        while True:
            try:
                buff = player.conn.recv(1024)
            
            except Exception as e:
                close_conn(client, addr, e)
                players_list.remove(player)
                break
    
    return


if __name__ == "__main__":
    
    players_list : list[ServerPlayer] = []
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    
    logging.info(f"Server is now listening on port: {PORT}")
    server.listen(5)

    while True:
        client_sock, addr = server.accept()
        logging.info(f"Client connected: {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        client_thread.start()


