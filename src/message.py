class Message:
    def __init__(self, byte_str: bytes):
        self.is_valid = byte_str != b''

        if byte_str != b'':
            self.line, byte_str = byte_str.split(b'\r\n', 1)
            header_fields, self.body = byte_str.split(b'\r\n\r\n', 1)
            
            self.headers = dict()
            for header in header_fields.split(b'\r\n'):
                header_key, header_val = header.split(b': ', 1)
                self.headers[header_key] = header_val

    def set_header(self, key: bytes, value: bytes):
        if value is None:
            self.headers.pop(key, None)
        else:
            self.headers[key] = value

    def get_header(self, key: bytes) -> bytes:
        return self.headers.get(key, None)

    def __bytes__(self) -> bytes:
        value = self.line + b'\r\n'
        for header_key, header_val in self.headers.items():
            value += header_key + b': ' + header_val + b'\r\n'
        value += b'\r\n' + self.body
        return value

    def __str__(self) -> str:
        bodyless = self.line + b'\r\n'
        for header_key, header_val in self.headers.items():
            bodyless += header_key + b': ' + header_val + b'\r\n'

        value = '-' * 64 + '\r\n'
        value += bodyless.decode()
        value += '-' * 64
        return value


def timeout_message(request: Message):
    _, _, version = request.line.split(b' ', 2)
    return Message(version + b' 408 Request Timeout\r\nAge: 0\r\n\r\n')


def timeout_message(request: Message):
    _, _, version = request.line.split(b' ', 2)
    return Message(version + b' 408 Request Timeout\r\nAge: 0\r\n\r\n')