from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from threading import Thread
from json import loads

from crypto_stream import StreamEncrypter
from generators import solitaire, blum_blum_shub

HOST = 'localhost'
EXIT = 'bye'
CONFIG = "config2.json"

PORT_CHOSEN = False
EXITED = False

def recv(server_socket: socket, decrypter: StreamEncrypter):
    with server_socket.accept()[0] as recv_socket:
        while True:
            e = recv_socket.recv(1024)
            data = decrypter(e).decode()
            if data == EXIT or data == '':
                break
            print("\nReceived: ", data)
            
            if not EXITED:
                print("> " if PORT_CHOSEN else "Peer port? ", end="", flush=True)
        


if __name__ == "__main__":
    my_port = int(argv[1])
    with open(CONFIG, "r") as file:
        config = loads(file.read())
        generator = solitaire if config["generator"] == "SOLITAIRE" else blum_blum_shub
        seed = config["seed"]
        encrypter = StreamEncrypter(seed, generator)

    with socket(AF_INET, SOCK_STREAM) as server_socket, socket(AF_INET, SOCK_STREAM) as send_socket:
        server_socket.bind(('', my_port))
        server_socket.listen()
        print("Listening on port", my_port)
        t1 = Thread(target= recv, args = (server_socket, encrypter))
        t1.start()

        peer_port = int(input("Peer port? "))
        send_socket.connect((HOST, peer_port))
        PORT_CHOSEN = True
        while True:
            data = input("> ")

            send_socket.send(encrypter(data.encode()))

            if data == EXIT:
                EXITED = True
                break

        t1.join()

    

