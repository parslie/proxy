from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, \
    SOMAXCONN, timeout
from threading import Thread

import color
from message import Message, timeout_message


def send_request(request: Message) -> Message:
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(15)

    host = request.get_header(b'Host')
    port = 80
    if b':' in host:
        host, port = host.split(b':')
        port = int(port)

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
    

def request_handler(id: int, connection: socket):
    request = Message(connection.recv(4096))
    
    if request.is_valid:
        request.set_header(b'User-Agent', b'Mozilla/5.0 (Linux x86_64; rv:96.0) \
            Gecko/20100101 Firefox/96.0')

        try:
            print(f'{id}: Sending {color.BOLD}({request.line.decode()}){color.END}...')
            response = send_request(request)
        except timeout:
            response = timeout_message(request)
            
        if response is not None:
            _, status_code, _ = response.line.split(b' ', 2)
            status_color = color.GREEN
            if status_code.startswith(b'3'):
                status_color = color.YELLOW
            elif status_code.startswith(b'4') or status_code.startswith(b'5'):
                status_color = color.RED

            print(f'{id}: {status_color}Received {color.BOLD}({response.line.decode()}){color.END}!')
            connection.sendall(bytes(response))

    connection.close()


def start_server(host: str, port: int):
    print('Starting server...')
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(SOMAXCONN)
    print('Server started!\r\n')
    
    thread_id = 0
    while True:
        connection, connection_addr = s.accept()
        thread = Thread(target=request_handler, args=[thread_id, connection], daemon=True)
        thread.start()
        thread_id += 1


if __name__ == '__main__':
    start_server('127.0.0.1', 8080)