from typing import Any
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, path
from threading import Thread
from time import sleep
import json
from random import shuffle

path.append('../lab2')

from constants import HOST, KEYSERVER_PORT, SET, GET, OK
from merkle_hellman import generate_knapsack_keypair, PublicKey, encrypt_mh, decrypt_mh
from crypto_classes import PrivateKeyDecrypter, PublicKeyEncrypter
from generators import solitaire
from crypto_stream import StreamEncrypter

class KeyServerException(Exception):
    pass

EXIT = 'bye'
HANDSHAKE_STARTED = False
PORT_CHOSEN = False
EXITED = False

mh_decrypter=None
mh_encrypter=None
symmetric_encrypter=None
peer_client_id=None

def generate_solitaire_key() -> list[int]:
    deck = [i + 1 for i in range(54)]
    shuffle(deck)
    return deck

def combine_solitaire_keys(deck1: list[int], deck2: list[int]) -> list[int]:
    return [deck2[card - 1] for card in deck1]

def send(socket: socket, encrypter: PublicKeyEncrypter, data: Any):
    e = encrypter(json.dumps(data).encode())
    socket.send(json.dumps(e).encode())

def receive(socket: socket, decrypter: PrivateKeyDecrypter) -> Any:
    e = json.loads(socket.recv(2048))
    return json.loads(decrypter(e))

def recv(server_socket: socket):
    global peer_client_id
    global mh_encrypter
    global HANDSHAKE_STARTED
    global symmetric_encrypter

    with server_socket.accept()[0] as recv_socket:
        if not HANDSHAKE_STARTED:
            HANDSHAKE_STARTED = True
            # hello: list[int] = json.loads(recv_socket.recv(1024))
            # msg: dict = json.loads(mh_decrypter(hello))
            hello: dict = receive(recv_socket, mh_decrypter)
            peer_client_id = hello['clientId']
            print('\nPeer client id =', peer_client_id)
            peer_public_key = get_client_public_key(peer_client_id)
            print('Peer public key =', peer_public_key)
            mh_encrypter = PublicKeyEncrypter(peer_public_key, encrypt_mh)

            send(recv_socket, mh_encrypter, {'msg': 'Ack'})
            # e = mh_encrypter(json.dumps({'msg': 'Ack'}).encode())
            # recv_socket.send(json.dumps(e).encode())

            my_solitaire_key = generate_solitaire_key()

            # e: list[int] = json.loads(recv_socket.recv(2048))
            # their_solitaire_key: dict = json.loads(mh_decrypter(e))
            their_solitaire_key = receive(recv_socket, mh_decrypter)
            print('Peer solitaire key', their_solitaire_key)

            send(recv_socket, mh_encrypter, my_solitaire_key)
            # e = mh_encrypter(json.dumps(my_solitaire_key).encode())
            # recv_socket.send(json.dumps(e).encode())

            common_solitaire_key = combine_solitaire_keys(my_solitaire_key, their_solitaire_key)
            print('Common solitaire key', common_solitaire_key)

            symmetric_encrypter = StreamEncrypter(common_solitaire_key, solitaire)

            print('Type anything to continue...')

        while True:
            e = recv_socket.recv(1024)
            data = symmetric_encrypter(e).decode()
            
            if data == EXIT or data == '':
                break
            print("\nReceived: ", data)
            
            if not EXITED:
                print("> ", end="", flush=True)


def register_to_keyserver(client_id: int, public_key: PublicKey):
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
            raise KeyServerException
        else:
            print('Successfully registered public key to keyserver')


def get_client_public_key(client_id: int) -> PublicKey:
    query = {
        'method': GET,
        'clientId': client_id,
    }

    with socket(AF_INET, SOCK_STREAM) as keyserver_socket:
        keyserver_socket.connect((HOST, KEYSERVER_PORT))
        keyserver_socket.send(json.dumps(query).encode())
        res: dict = json.loads(keyserver_socket.recv(1024))

        if res.get('status') != OK:
            raise KeyServerException
        else:
            return res.get('publicKey')


def init_handshake(socket: socket, client_id: int):
    global mh_encrypter
    global HANDSHAKE_STARTED
    global symmetric_encrypter

    HANDSHAKE_STARTED = True
    send(socket, mh_encrypter, {'clientId': client_id})
    # e = mh_encrypter(json.dumps({'clientId': client_id}).encode())
    # socket.send(json.dumps(e).encode())

    # e = json.loads(socket.recv(1024))
    # msg: dict = json.loads(mh_decrypter(e))
    ack = receive(socket, mh_decrypter)
    print("Received ack", ack)

    my_solitaire_key = generate_solitaire_key()

    send(socket, mh_encrypter, my_solitaire_key)
    # e = mh_encrypter(json.dumps(my_solitaire_key).encode())
    # socket.send(json.dumps(e).encode())

    # e: list[int] = json.loads(socket.recv(2048))
    # their_solitaire_key: dict = json.loads(mh_decrypter(e))
    their_solitaire_key: dict = receive(socket, mh_decrypter)
    print('Peer solitaire key', their_solitaire_key)

    common_solitaire_key = combine_solitaire_keys(their_solitaire_key, my_solitaire_key)
    print('Common solitaire key', common_solitaire_key)

    symmetric_encrypter = StreamEncrypter(common_solitaire_key, solitaire)


    


if __name__ == '__main__':
    my_port = int(argv[1])
    private_key, public_key = generate_knapsack_keypair()
    print('Private key =', private_key)
    print('Public key =', public_key)

    register_to_keyserver(my_port, public_key)

    mh_decrypter = PrivateKeyDecrypter(private_key, decrypt_mh)
    
    with socket(AF_INET, SOCK_STREAM) as server_socket, socket(AF_INET, SOCK_STREAM) as send_socket:
        server_socket.bind(('', my_port))
        server_socket.listen()
        print("Listening on port", my_port)
        t1 = Thread(target= recv, args = (server_socket,))
        t1.start()
        
        command = input("Peer client_id? ")
        if peer_client_id is None:
            peer_client_id = int(command)
            peer_public_key = get_client_public_key(peer_client_id)
            print('Public key of peer client =', peer_public_key)
            mh_encrypter = PublicKeyEncrypter(peer_public_key, encrypt_mh)
        
        send_socket.connect((HOST, peer_client_id))
        
        if not HANDSHAKE_STARTED:
            init_handshake(send_socket, my_port)

        while True:
            data = input("> ")

            send_socket.send(symmetric_encrypter(data.encode()))

            if data == EXIT:
                EXITED = True
                break

        t1.join()
    
    