from socket import error as Error

class ProtocolHandler(object):
    def __init__(self):
        self.data = {}

    def handle_request(self, fh):
        request = fh.readline().strip()
        if not request:
            return Error('No response from server')
        command, *args = request.split()
        if command == b'GET':
            key = args[0]
            if key in self.data:
                return self.data[key]
            else:
                return Error('Key not found')
        elif command == b'SET':
            key, value = args
            self.data[key] = value
            return b'OK'
        else:
            return Error('Unknown command')