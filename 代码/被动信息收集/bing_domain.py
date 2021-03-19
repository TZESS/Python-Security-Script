# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys
import argparse

def bing_search(site,pages):
    Subdomain=[]
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
               'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip,deflate',
               'referer': "https://cn.bing.com/"
               }
    for i in range(1,int(pages)+1):
        #'https://cn.bing.com/search?q=site:'+site+'&first='+i+'&FORM=PERE'
        url="https://cn.bing.com/search?q=site%3a"+site+'&first='+str((i-1)*10)+'&FORM=PERE'
        conn=requests.session()
        conn.get('https://cn.bing.com',headers=headers)
        html=conn.get(url,stream=True,headers=headers,timeout=8)
        soup=BeautifulSoup(html.content,'html.parser')
        job_bt=soup.findAll('h2')
        for i in job_bt:
            try:
                link=i.a.attrs['href']
            except AttributeError as e:
                pass
            finally:
                domain=str(urlparse(link).scheme+"://"+urlparse(link).netloc)
                if domain in Subdomain or domain =="://":
                    pass
                else:
                    Subdomain.append(domain)
                    print(domain)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="cn.bing collect domains")
    parser.add_argument('-u', '--url', required=True, type=str, help='input domain')
    parser.add_argument('-p', '--page', default ='10',type=str, help='input bing page numbers("default is 10")')  
    args = parser.parse_args()
    bing_search(args.url,args.page)