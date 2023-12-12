from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from threading import Thread
from json import loads

from constants import HOST, KEYSERVER_PORT, REGISTER, REQUIRE

if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as keyserver_socket:
        keyserver_socket.connect((HOST, KEYSERVER_PORT))
        # keyserver_socket.send(b'REGISTER:my_id my_key')
        keyserver_socket.send(b'REQUIRE:my_id')
        print(keyserver_socket.recv(1024).decode())