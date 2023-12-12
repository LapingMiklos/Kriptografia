from socket import socket, AF_INET, SOCK_STREAM
from merkle_hellman import PublicKey
import json

from constants import HOST, KEYSERVER_PORT, SET, GET, OK

class KeyServerException(Exception):
    pass

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


def test_keyserver():
    public_keys = {
        1: 'some ket',
        2: 'other key',
        3: [1,3,4324243213],
        4: 5,
        'someid': 'somekey'
    }

    for client_id, public_key in public_keys.items():
        register_to_keyserver(client_id, public_key)
    
    for client_id in public_keys:
        assert get_client_public_key(client_id) == public_keys[client_id]
    
    try:
        get_client_public_key('INVALID_ID')
    except KeyServerException:
        print('No public key found for id=INVALID_ID')
        pass


if __name__ == '__main__':
    test_keyserver()