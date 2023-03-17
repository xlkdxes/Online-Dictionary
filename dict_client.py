import sys
from socket import *


class DictHandle:
    def __init__(self):
        self.socket = self.create_socket()

    def create_socket(self):
        s = socket()
        s.connect(('127.0.0.1', 7777))
        return s

    def do_register(self):
        username = input('Username:')
        password = input('Password:')
        msg = 'R %s %s' % (username, password)
        self.socket.send(msg.encode())
        res = self.socket.recv(128)
        if res == b'T':
            print('Register Successfully')
            return True
        elif res == b'F':
            print('Register Failed')
            return False

    def do_login(self, username, password):
        msg = 'L %s %s' % (username, password)
        self.socket.send(msg.encode())
        res = self.socket.recv(128)
        if res == b'T':
            print('Login Successfully')
            return True
        elif res == b'F':
            print('Login Failed')
            return False

    def do_query(self):
        while True:
            word = input('Query: ')
            if word == '##':
                break
            msg = "Q " + word
            self.socket.send(msg.encode())
            res = self.socket.recv(1024).decode()
            temp = res.split(' ', 1)
            if temp[0] == 'T':
                print(temp[1] + '\n')
            else:
                print('Not Found\n')

    def do_history(self):
        self.socket.send(b'H')
        res = self.socket.recv(1024 * 1024).decode()
        temp = res.split(' ', 1)
        if temp[0] == 'T':
            for r in temp[1].split(';'):
                print(r)
        else:
            print('No history')

    def do_exit(self):
        self.socket.send(b'E')
        self.socket.close()
        sys.exit('Thanks')


class DictView:
    def __init__(self):
        self.handle = DictHandle()

    def first_view(self):
        while True:
            c = input("""
                =================== Online Dictionary ===================
                =================== 1. Register =========================
                =================== 2. Login ============================
                =================== 3. Quit =============================
            """)
            if c == '1':
                self.handle.do_register()
            elif c == '2':
                username = input('Username:')
                password = input('Password:')
                if self.handle.do_login(username, password):
                    self.second_view(username)
            elif c == '3':
                self.handle.do_exit()

    def second_view(self, name):
        while True:
            c = input("""
                =============== %s's Online Dictionary ===============
                =============== 1. Query =============================
                =============== 2. History ===========================
                =============== 3. Quit ==============================
            """ % name)
            if c == '1':
                self.handle.do_query()
            elif c == '2':
                self.handle.do_history()
            elif c == '3':
                break


if __name__ == '__main__':
    d = DictView()
    d.first_view()
