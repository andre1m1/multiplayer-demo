import socket
import threading
import random
import json
import logging
from common import *


type Err = Exception | None

class Player(PlayerCommon):
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



def handle_client(client : socket.socket, addr : str) -> None:
    try:
        client.sendall(json.dumps({"type" : "hello"}).encode("utf-8"))

        hello_msg : dict = json.loads(client.recv(1024))

        if hello_msg["type"] != "hello":
            close_conn(client, addr)
            return
        
        player = Player(random.randrange(WIDTH), random.randrange(HEIGHT), client)
        players_list.append(player)

        player.conn.sendall(json.dumps({
            "type": "pos",
            "x": player.x,
            "y": player.y
        }).encode("utf-8"))



    except Exception as e:
        close_conn(client, addr, e)
        return

    while True:
        try:
            buff = player.conn.recv(1024)
        
        except Exception as e:
            close_conn(client, addr, e)
            break
        

if __name__ == "__main__":
    
    players_list : list[Player] = []
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    
    logging.info(f"Server is now listening on port: {PORT}")
    server.listen(5)

    while True:
        client_sock, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        client_thread.start()


