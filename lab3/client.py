from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from threading import Thread
import json

from constants import HOST, KEYSERVER_PORT, REGISTER, REQUIRE, SET, GET
from merkle_hellman import generate_knapsack_keypair

def main():
    private_key, public_key = generate_knapsack_keypair()
    print('Private key =', private_key)
    print('Public key =', public_key)

    query = {
        'method': SET,
        'clientId': 'my_client_id2',
        'publicKey': public_key
    }
    ser = json.dumps(query).encode()
    print(ser)

    with socket(AF_INET, SOCK_STREAM) as keyserver_socket:
        keyserver_socket.connect((HOST, KEYSERVER_PORT))
        keyserver_socket.send(ser)
        print(json.loads(keyserver_socket.recv(1024)))
    



if __name__ == '__main__':
    main()
    