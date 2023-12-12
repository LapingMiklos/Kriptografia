from socket import socket, AF_INET, SOCK_STREAM
from constants import HOST, KEYSERVER_PORT, REGISTER, REQUIRE

if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, KEYSERVER_PORT))
        server_socket.listen()
        print('Listening on port', KEYSERVER_PORT)
        public_keys: dict[str, str] = {}
        while True:
            with server_socket.accept()[0] as client_socket:
                msg = client_socket.recv(1024).decode()
                # REGISTER: client_id public_key | REQUIRE: client_id
                print('Received message', msg)
                tokens = msg.split(':')
                if len(tokens) != 2:
                    client_socket.send(b'Incorrect query')
                    print('Incorrect')
                    continue

                query, data = tokens
                if query == REGISTER:
                    tokens = data.split()
                    if len(tokens) != 2:
                        client_socket.send(b'Incorrect query')
                        print('Incorrect 2')
                    else:
                        client_id, public_key = tokens
                        public_keys[client_id] = public_key
                        print('New keys', public_keys)
                elif query == REQUIRE:
                    client_socket.send(public_keys.get(data, 'Key not found').encode())

