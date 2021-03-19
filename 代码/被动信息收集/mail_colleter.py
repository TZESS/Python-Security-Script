import requests
from bs4 import BeautifulSoup
import re
import sys
import getopt
import pyfiglet
from urllib.parse import quote
import time
import threading

class MyThread(threading.Thread):
    def __init__(self,target,args=(),name=""):
        super().__init__(target=target, args=args, name='')
    
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

def banner(string):
    ascii_banner = pyfiglet.figlet_format(string)
    print(ascii_banner)

def help():
    print("-h: --help :help info")
    print("-u: --url  :target url")
    print("-p: --page :search engine pages")
    print(f"eg: {sys.argv[0]} -u baidu.com -p 100 ")
    sys.exit()

def launcher(url, pages):
    threads = []
    email_num = []
    key_words = ['email', 'mail', 'mailbox', '邮件', '邮箱', 'postbox']
    for key_word in key_words:
        for page in range(1, int(pages) + 1):
            t = MyThread(target=emails, args=(url, page, key_word))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()
    for email in allemails:
        if email in email_num:
            pass
        else:
            print(email)
            with open('data.txt', 'a+') as f:
                f.write(email + "\n")
            email_num.append(email)

def emails(url, page, key_word):
    global allemails
    allemails = []
    bing_emails = bing_search(url, page, quote(key_word))
    baidu_emails = baidu_search(url, page, quote(key_word))
    sum_emails = bing_emails + baidu_emails
    for i in sum_emails:
        allemails.append(i)
    #print(allemails)
    return sum_emails

def bing_search(url, page, key_word):                                           #bing只在搜索页查找
    #print("bing 当前页面数:" + str(page) + ":关键词" + key_word)
    referer = "https://www.baidu.com/s?wd=email+site%3Abaidu.com&pn=1"
    conn = requests.session()
    bing_url = f"https://cn.bing.com/search?q={key_word}+site%3a{url}&qs=n&sp=-1&pq={key_word}+site%3a{url}&first={str(int(page-1)*10)}&FORM=PERE"
    conn.get('https://cn.bing.com', headers=header(referer))
    r = conn.get(bing_url, stream=True, headers=header(referer), timeout=8)
    emails = search_email(r.text)
    return emails

def baidu_search(url, page, key_word):                                          #baidu在搜索页打开链接，然后查找
    #print("baidu 当前页面数:" + str(page) + ":关键词" + key_word)
    email_list = []
    emails = []
    #proxy={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}
    referer = "https://www.baidu.com/s?wd=email+site%3Abaidu.com&pn=1"
    baidu_url = "https://www.baidu.com/s?wd=" + key_word + "+site%3A" + url + "&pn=" + str((page - 1) * 10)
    conn = requests.session()
    conn.get(referer, headers=header(referer))
    r = conn.get(baidu_url, headers=header(referer))
    bs = BeautifulSoup(r.text, "lxml")
    title=bs.findAll('h3')
    for h3 in title:
        href=h3.find('a').get('href')
        try:
            r = requests.get(href, headers=header(referer), timeout=8)
            emails = search_email(r.text)
        except Exception as e:
            pass
        for email in emails:
            email_list.append(email)
    return email_list

def header(referer):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip,deflate',
    'referer': referer
    }
    return headers

def search_email(html):
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",html,re.I)
    return emails    

def main(args):
    url = ""
    pages = ""
    if len(args) < 2:
        print(len(args))
        help()
        sys.exit()
    try:
        banner("Email Colletor")
        opts,args=getopt.getopt(args,"-u:-p:-h-v",['url','page','help','version'])
    except getopt.GetoptError:
        print("Error an argument")
        sys.exit()
    for opt, arg in opts:
        if opt in ("-u", "--url"):
            url = arg
        if opt in ("-p", "--page"):
            pages = arg
        if opt in ("-h", "--help"):
            help()
        if opt in ("-v", "--version"):
            print("version: 1.0")
    launcher(url, pages)

if __name__ == "__main__":
    start=time.time()
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("interupted by user")
    end = time.time()
    print("Use :"+str(end-start)+" Seconds")