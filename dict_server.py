from socket import *
from threading import Thread
from dict_db import *


class Handle:
    def __init__(self, conn, db):
        self.conn = conn
        self.db = db
        self.name = None

    def do_register(self, username, password):
        if self.db.register(username, password):
            self.conn.send(b'T')
        else:
            self.conn.send(b'F')

    def do_login(self, username, password):
        if self.db.login(username, password):
            self.conn.send(b'T')
            self.name = username
        else:
            self.conn.send(b'F')

    def do_query(self, word):
        explaination = self.db.query(word, self.name)
        if explaination:
            msg = "T " + explaination
            self.conn.send(msg.encode())
        else:
            msg = "F"
            self.conn.send(msg.encode())

    def do_history(self):
        data = self.db.history(self.name)
        if data:
            msg = 'T '
            for i in data:
                word = '%s,%s,%s;' % i
                msg += word
            self.conn.send(msg.encode())
        else:
            self.conn.send(b'F')

    def do_request(self):
        while True:
            req = self.conn.recv(1024).decode()
            temp = req.split(' ')
            if not req or temp[0] == 'E':
                break
            elif temp[0] == 'R':
                self.do_register(temp[1], temp[2])
            elif temp[0] == 'L':
                self.do_login(temp[1], temp[2])
            elif temp[0] == 'Q':
                self.do_query(temp[1])
            elif temp[0] == 'H':
                self.do_history()


class DictThread(Thread):
    def __init__(self, conn):
        self.conn = conn
        self.db = DictDB()
        self.handle = Handle(conn, self.db)
        super().__init__(daemon=True)

    def run(self):
        self.handle.do_request()
        self.conn.close()
        self.db.close()


class DictServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.addr = (host, port)
        self.socket = self._create_socket()

    def _create_socket(self):
        s = socket()
        s.bind(self.addr)
        return s

    def start_server(self):
        self.socket.listen(5)
        while True:
            conn, addr = self.socket.accept()
            print('Connect From: ' + str(addr))
            p = DictThread(conn)
            p.start()


if __name__ == '__main__':
    d = DictServer('127.0.0.1', 7777)
    d.start_server()
