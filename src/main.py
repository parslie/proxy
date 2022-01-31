from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, \
    SOMAXCONN
from threading import Thread

from message import Request


def request_handler(connection: socket):
    request = Request(connection.recv(4096))
    
    if request.is_valid:
        print(request)
        request.set_header(b'User-Agent', b'Mozilla/5.0 (Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0')

    connection.close()


def main(host: str, port: int):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((host, port))

    s.listen(SOMAXCONN)

    while True:
        connection, connection_addr = s.accept()
        thread = Thread(target=request_handler, args=[connection], daemon=True)
        thread.start()


if __name__ == '__main__':
    main('127.0.0.1', 8080)