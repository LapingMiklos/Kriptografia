from typing import Any
from socket import socket, AF_INET, SOCK_STREAM
import json

from constants import HOST, KEYSERVER_PORT, REGISTER, REQUIRE, GET, SET, OK, NOT_OK

def resolve_query(client_socket: socket, public_keys: dict):
    def send_error(**kwargs: dict):
        kwargs['status'] = NOT_OK
        client_socket.send(json.dumps(kwargs).encode())
        print('Sent error message to client', kwargs)

    def send_ok(**kwargs: dict):
        kwargs['status'] = OK
        client_socket.send(json.dumps(kwargs).encode())
        print('Sent response to client', kwargs)

    try:
        query: dict = json.loads(client_socket.recv(1024))
        method = query.get('method')
        if method == SET:
            client_id = query.get('clientId')
            public_key = query.get('publicKey')
            if client_id is None or public_key is None:
                send_error(msg=f'clientId={client_id}, publicKey={public_key} is invalid')
            else:
                public_keys[client_id] = public_key
                send_ok()
        elif method == GET:
            client_id = query.get('clientId')
            if client_id is None:
                send_error(msg=f'clientId not given')
                return
            
            public_key = public_keys.get(client_id)
            if public_key is None:
                send_error(msg=f'client with id={client_id} does not exist')
            else:
                send_ok(clientId=client_id)
        else:
            send_error(msg=f'Invalid method={method}')
    except json.JSONDecodeError:
        send_error(msg='Invalid query format')

def main():
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, KEYSERVER_PORT))
        server_socket.listen()
        print('Listening on port', KEYSERVER_PORT)
        public_keys: dict = {}

        while True:
            with server_socket.accept()[0] as client_socket:
                resolve_query(client_socket, public_keys)
                print(public_keys)
                

if __name__ == '__main__':
    main()

