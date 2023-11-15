from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from threading import Thread

from crypto_stream import StreamEncrypter
from generators import solitaire, blum_blum_shub

HOST = 'localhost'

def recv(server_socket: socket):
    recv_socket, address = server_socket.accept()
    print(address)
    while True:
        data = recv_socket.recv(1024).decode()
        if data == 'EXIT':
            exit()
        print(data)



if __name__ == "__main__":
    my_port = int(argv[1])
    with socket(AF_INET, SOCK_STREAM) as server_socket, socket(AF_INET, SOCK_STREAM) as send_socket:
        server_socket.bind(('', my_port))
        server_socket.listen()
        print("Listening on port", my_port)
        t1 = Thread(target= recv, args = (server_socket,))
        t1.start()

        peer_port = int(input("Peer port? "))
        send_socket.connect((HOST, peer_port))
        
        while True:
            data = input("Send something: ")

            send_socket.send(data.encode())

            if data == "EXIT":
                break

        t1.join()

    

