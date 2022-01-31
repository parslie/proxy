from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, \
    SOMAXCONN, timeout
from threading import Thread

from message import Message, timeout_message


def send_request(request: Message) -> Message:
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(12)

    host = request.get_header(b'Host')
    port = 80
    if b':' in host:
        host, port = host.split(b':')
        port = int(port)
        print(request)
    #    return None

    s.connect((host, port))
    s.sendall(bytes(request))

    response_bytes = b''
    while True:
        data = s.recv(1024)
        if len(data) <= 0:
            break
        response_bytes += data

    s.close()
    return Message(response_bytes)
    

def request_handler(connection: socket):
    request = Message(connection.recv(4096))
    
    if request.is_valid:
        request.set_header(b'User-Agent', b'Mozilla/5.0 (Linux x86_64; rv:96.0) \
            Gecko/20100101 Firefox/96.0')

        try:
            response = send_request(request)
        except timeout:
            response = timeout_message(request)
            
        if response is not None:
            connection.sendall(bytes(response))

    connection.close()


def start_server(host: str, port: int):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((host, port))

    s.listen(SOMAXCONN)

    while True:
        connection, connection_addr = s.accept()
        thread = Thread(target=request_handler, args=[connection], daemon=True)
        thread.start()


if __name__ == '__main__':
    start_server('127.0.0.1', 8080)