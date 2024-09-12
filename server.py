import socket
import threading
import random
import json
import logging
from common import *



id_count = 0
def iota():
    global id_count
    id_count += 1
    return id_count

class ServerPlayer(Player):
    def __init__(self, x: int, y: int, color: Color, conn: socket.socket) -> None:
        super().__init__(x, y, iota(), color, conn)


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
            "y" : player.y,
            "id" : player.id,
            "color" : player.color
        })

    return players


def broadcast_msg(msg: dict, exclude=None) -> None:
    for p in players_list:
        if p.conn is not None and p.id != exclude:
            p.conn.sendall(json.dumps(msg).encode("utf-8"))


def get_random_color() -> Color:
    return (random.randrange(255), random.randrange(255), random.randrange(255))

def handle_connection(client : socket.socket, addr : str) -> ServerPlayer | None:
    try:
        client.sendall(json.dumps({"type" : MessageType.HELLO.value}).encode("utf-8"))

        hello_msg : dict = json.loads(client.recv(1024))

        if hello_msg["type"] != MessageType.HELLO.value:
            close_conn(client, addr)
            return None

        player = ServerPlayer(random.randrange(WIDTH-PLAYER_SIZE), random.randrange(HEIGHT - PLAYER_SIZE), get_random_color(), conn=client)

        if player.conn is None:
            raise Exception("Could not receive client connection!")

        player.conn.sendall(json.dumps({
            "type" : MessageType.INIT.value,
            "x": player.x,
            "y": player.y,
            "id": player.id,
            "color": player.color,
            "players" : serialize_players(players_list)
        }).encode("utf-8"))

        players_list.append(player)

        broadcast_msg({
            "type" : MessageType.PLAYER_JOINED.value,
            'x' : player.x,
            'y' : player.y,
            "id": player.id,
            "color": player.color
        }, exclude=player.id)

        return player

    except Exception as e:
        close_conn(client, addr, e)
        players_list.remove(player)
        return None


def handle_client(client : socket.socket, addr : str) -> None:
    player = handle_connection(client, addr)

    if type(player) == ServerPlayer and player.conn is not None: 
        while True:
            try:
                msg = json.loads(player.conn.recv(1024))
                match msg["type"]:
                    case MessageType.PLAYER_LEFT.value:
                        close_conn(player.conn, addr)
                        players_list.remove(player)
                        broadcast_msg({
                            "type" : MessageType.PLAYER_LEFT.value,
                            "id" : player.id
                        })
                        break

                    case MessageType.PLAYER_MOVE.value:
                        for move in msg["moves"]:
                            if 'x' in move:
                                player.x += move['x']
                            else:
                                player.y += move['y']

                        broadcast_msg({
                            "type" : MessageType.PLAYER_MOVE.value,
                            "id" : player.id,
                            "pos" : (player.x, player.y)
                        }, exclude=player.id)

                    case _:
                        raise Exception("Unknown Message received from client")

            
            except Exception as e:
                close_conn(client, addr, e)
                players_list.remove(player)
                break


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


