import os
import re
import json
import subprocess
import time

with open('logs/alog', 'r+') as f:
    while True:
        str = f.readline().rstrip('\n')
        if len(str) != 0: 
            output = json.loads(str)[0][1]
            print(output, end='')
            time.sleep(0.1)
        else: break
