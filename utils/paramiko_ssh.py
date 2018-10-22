# -*- coding:utf-8 -*-
import paramiko 
import os 
import select 
import sys 
import tty 
import termios 
import json


def run(ipaddr, port, user, passwd):
    trans = paramiko.Transport((ipaddr, int(port))) 
    trans.start_client() 

    trans.auth_password(username=user, password=passwd) 
    channel = trans.open_session() 
    channel.get_pty() 
    channel.invoke_shell() 

    oldtty = termios.tcgetattr(sys.stdin) 

    try: 
        tty.setraw(sys.stdin) 
        channel.settimeout(0) 

        while True: 
            readlist, writelist, errlist = select.select([channel, sys.stdin,], [], []) 
            
            input_cmdstr = []
            if sys.stdin in readlist: 
                input_cmd = sys.stdin.read(1) 
                channel.sendall(input_cmd) 

            if channel in readlist: 
                result = channel.recv(1024) 
                if len(result) == 0: 
                    print("\r\n**** EOF **** \r\n") 
                    break 
                sys.stdout.write(result.decode()) 
                with open('/opt/jumpserver/logs/alog', 'a+') as f:
                    list = [('time', result.decode())]
                    f.write(json.dumps(list))
                    f.write('\n')
                sys.stdout.flush() 
    finally: 
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty) 

    channel.close() 
    trans.close()
