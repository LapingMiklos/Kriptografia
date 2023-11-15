from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from threading import Thread
from json import loads

from crypto_stream import StreamEncrypter
from generators import solitaire, blum_blum_shub

HOST = 'localhost'
EXIT = 'bye'
CONFIG = "config2.json"

def recv(server_socket: socket, decrypter: StreamEncrypter):
    recv_socket, _ = server_socket.accept()
    while True:
        e = recv_socket.recv(1024)
        data = decrypter(e).decode()
        if data == EXIT:
            recv_socket.close()
            break
        print("\nReceived: ", data)
        print("> ", end="", flush=True)
        


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
        
        while True:
            data = input("> ")

            send_socket.send(encrypter(data.encode()))

            if data == EXIT:
                break

        t1.join()

    

