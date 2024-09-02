import socket
import threading
import json
import logging
from common import *


type Err = Exception | None


class Player(PlayerCommon):
    def __init__(self, x, y, conn) -> None:
        super().__init__(x, y, conn)



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

        hello_msg = client.recv(1024)
        hello_msg : dict = json.loads(hello_msg)

        if hello_msg["type"] != "hello":
            close_conn(client, addr)
        else:
            print(hello_msg)


    except Exception as e:
        close_conn(client, addr, e)

    while True:
        try:
            pass
        
        except Exception as e:
            close_conn(client, addr, e)
            break
        
if __name__ == "__main__":
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


