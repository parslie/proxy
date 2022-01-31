class Request:
    def __init__(self, byte_str: bytes):
        self.is_valid = byte_str != b''

        if byte_str != b'':
            request_line, byte_str = byte_str.split(b'\r\n', 1)
            header_fields, self.body = byte_str.split(b'\r\n\r\n', 1)
            
            self.method, self.url, self.version = request_line.split(b' ')
            self.headers = dict()

            for header in header_fields.split(b'\r\n'):
                header_key, header_val = header.split(b': ')
                self.headers[header_key] = header_val

    def set_header(self, key: bytes, value: bytes):
        if value is None:
            self.headers.pop(key, None)
        else:
            self.headers[key] = value

    def get_header(self, key: bytes) -> bytes:
        return self.headers.get(key, None)

    def __bytes__(self) -> bytes:
        value = self.method + b' ' + self.url + b' ' + self.version + b'\r\n'
        for header_key, header_val in self.headers.items():
            value += header_key + b': ' + header_val + b'\r\n'
        value += b'\r\n' + self.body
        return value

    def __str__(self) -> str:
        value = '-' * 64 + '\r\n'
        value += self.__bytes__().decode('utf-8')
        value += '-' * 64
        return value