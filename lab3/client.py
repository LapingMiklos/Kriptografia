from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from threading import Thread
import json

from constants import HOST, KEYSERVER_PORT, SET, GET, OK
from merkle_hellman import generate_knapsack_keypair

class InvalidRegistationException(Exception):
    pass

def register_to_keyserver(client_id: int, public_key):
    query = {
        'method': SET,
        'clientId': client_id,
        'publicKey': public_key
    }

    with socket(AF_INET, SOCK_STREAM) as keyserver_socket:
        keyserver_socket.connect((HOST, KEYSERVER_PORT))
        keyserver_socket.send(json.dumps(query).encode())
        res: dict = json.loads(keyserver_socket.recv(1024))

        if res.get('status') != OK:
            raise InvalidRegistationException
        else:
            print('Successfully registered public key to keyserver')

def main():
    my_port = int(argv[1])
    private_key, public_key = generate_knapsack_keypair()
    print('Private key =', private_key)
    print('Public key =', public_key)

    register_to_keyserver(my_port, public_key)
    



if __name__ == '__main__':
    main()
    