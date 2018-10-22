# -*- coding:utf-8 -*-
import sys
import getpass
import json
import os
from utils import paramiko_ssh
from urllib import request, error, parse

class main():
    @classmethod
    def ArgsHandler(cls, arg):
        if arg == 'run':
            return Session();

class Session():
    def __init__(self):
        self.hostlist = []
        self.hostinfo = []
        self.hostname = ''
        self.url_prefix = 'http://192.168.0.100:8000'

    def run(self):
        print('######################################')
        print('Welcome to Jumpserver, Please Login...')
        print('######################################')
        while True:
            print('')
            username = input('username: ')
            password = getpass.getpass('password: ')
            if self.auth(username, password):
                self.username = username
                self.host_choice()
            else:
                print('AUTH FAILED...input again...')

    def auth(self, username, password):
        url = self.url_prefix + '/jumpserver/auth'
        data = {'username':username, 'password': password}
        return self.data_trans(data, url, 'auth')

    def data_trans(self, data, url, mode):
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url)

        try:
            if mode == 'auth':
                self.hostlist = json.loads(request.urlopen(req, data=data).read().decode('utf-8'))
            elif mode == 'getaccount':
                self.hostinfo = json.loads(request.urlopen(req, data=data).read().decode('utf-8'))
        except error.URLError as e:
            print(e)
            return False
        except error.HTTPError as e:
            print(e.code)
            print(e.read().decode('utf-8'))
            return False
        
        if self.hostlist or self.hostinfo:
            return True

    def host_choice(self):
        while True:
            print('')
            for i in range(1, len(self.hostlist)+1):
                print("({}) {} | {} | {}".format(i, self.hostlist[i-1][0], self.hostlist[i-1][1], self.hostlist[i-1][2]))
            print('')
            choice = input("input your choice: ")
            if choice == 'exit':
                sys.exit(255)
            try:
                choice = int(choice)
                if choice > 0 and choice <= len(self.hostlist):
                    self.get_account(self.hostlist[choice-1])
                else:
                    print("NOT VALID CHOICE...input again...")
            except Exception as e:
                print(e)
                print('ERROR...input again...')

    def get_account(self, hostlist):
        url = self.url_prefix + '/jumpserver/getaccount'
        self.data_trans({'hostlist':hostlist}, url, 'getaccount')
        ipaddr, port, user, passwd = self.hostinfo[0][0], self.hostinfo[0][1], self.hostinfo[0][2], self.hostinfo[0][3]
        os.system('clear')
        paramiko_ssh.run(ipaddr, port, user, passwd)
        os.system('clear')
        print('######################################')
        print('Welcome to Jumpserver, Please Login...')
        print('######################################')
        print('')
        print('username: {}'.format(self.username))
        print('password: ')



if __name__ == '__main__':
    Session = main.ArgsHandler(sys.argv[1])
    Session.run()








