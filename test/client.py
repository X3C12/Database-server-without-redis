from gevent import socket
from socket import error as socket_error

from collections import namedtuple

import protocolHandler as pH

class CommandError(Exception): pass

Error = namedtuple('Error', ('message',))

class Client(object):
    def __init__(self, host='127.0.0.1', port=8080):
        self._protocol = pH.ProtocolHandler()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._fh = self._socket.makefile('rwb')

    
    def execute(self, *args):
        request = b' '.join(args) + b'\n'
        self._fh.write(request)
        self._fh.flush()
        resp = self._protocol.handle_request(self._fh)

        if isinstance(resp, Error):
            raise CommandError(resp.message)

        if isinstance(resp, tuple):
            return resp.join(str(x) for x in resp)
        else:
            return resp
    
    def get(self, key):
        return self.execute(b'GET', key)

    def set(self, key, value):
        return self.execute(b'SET', key, value)

    def delete(self, key):
        return self.execute(b'DELETE', key)

    def flush(self):
        return self.execute(b'FLUSH')
    
    def mget(self, *keys):
        return self.execute(b'MGET', *keys)

    def mset(self, *items):
        return self.execute(b'MSET', *items)
    
if __name__ == '__main__':
    from gevent import monkey; monkey.patch_all()
    client = Client()
    client.set(b'my_key', b'my_value')
    print(client.get(b'my_key'))  # Should print b'my_value'