import socket
from socket import error as Error

class ProtocolHandler(object):
    def __init__(self, file_path):
        self.data = {}
        self.file_path = file_path

    def handle_request(self, fh):
        request = fh.readline().strip()
        command, *args = request.split()
        if command == b'GET':
            key = args[0]
            try:
                with open(self.file_path, 'r') as f:
                    for line in f:
                        if line.startswith(key.decode() + ':'):
                            return line.strip().encode()
            except FileNotFoundError:
                return Error('File not found')
            return Error('Key not found')
        elif command == b'SET':
            key, value = args
            with open(self.file_path, 'a') as f:
                f.write('{}:{}\n'.format(key.decode(), value.decode()))
            return b'OK'
        else:
            return Error('Unknown command')

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 8080))
    sock.listen(1)
    conn, addr = sock.accept()
    fh = conn.makefile('rwb')
    protocol = ProtocolHandler('data.txt')  # Replace 'data.txt' with your file path
    while True:
        request = fh.readline().strip()
        if not request:
            break
        response = protocol.handle_request(fh)
        protocol.write_response(fh, response)
    conn.close()

if __name__ == '__main__':
    main()