import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt

def main():
    baseurl="https://movie.douban.com/top250?start="
    datalist=getData(baseurl)
    saveData(datalist,'test.xls')
    

def askURL(url):
    head={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode('utf-8')
        #print(html)
    except urllib.error.URLError as e:
        #避免如404错误
        if hasattr(e,"code"):
            print(e.code)
        #避免如url格式错误   
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def getData(baseurl):
    datalist=[]
    for i in range(0,10):
        #最后到达页面225，会显示225~250
        url=baseurl+str(i*25)
        html=askURL(url)
        #解析
        bs=BeautifulSoup(html,'html.parser')
        for item in bs.find_all('div',class_="item"):       #遍历每一个item(即每一部电影标签)
            data=[]
            item=str(item)      #从bs4.element.Tag变为str类，方便使用正则
            #这里使用正则搜索，而不是item.find('a').attrs['href']，效果是一样的
            
            link=re.findall(findLink,item)[0]   #获取连接。注意使用索引[0]，因为返回是一个只有一个元素的列表
            data.append(link)
            
            img=re.findall(findImgSrc,item)[0]
            data.append(img)
            
            title=re.findall(findTitle,item)
            if(len(title)==2):
                chnTitle=title[0]           #中文名
                data.append(chnTitle)
                forTitle=title[1].replace("/","")   #外文名
                out="".join(forTitle.split())       #处理\xa0问题(即&nbsp;)，如"\xa0\xa0The Shawshank Redemption"
                data.append(out)
            else:
                data.append(title[0])
                data.append(' ')        #为了保存数据，即使不存在外文名，也必须要留空处理
            
            rating=re.findall(findRating,item)[0]
            data.append(rating)
            
            judge=re.findall(findJudge,item)[0]
            data.append(judge)
            
            inq=re.findall(findInq,item)     #电影的一句话评价可能不存在
            if (len(inq)) != 0:
                inq=inq[0].replace("。","")  #去除句号
                data.append(inq)
            else:
                data.append(" ")        #注意留空
            
            bd=re.findall(findBd,item)[0]
            bd=re.sub('<br/>\s*',"",bd)     #去除<br/>后面的其他符号内容
            bd=bd.strip()                   #去除空格
            bd="".join(bd.split())          #去除\xa0
            data.append(bd)
            datalist.append(data)
    return datalist

def saveData(datalist,savepath):
    print("Saving....")
    book=xlwt.Workbook(encoding="utf-8",style_compression=0)          #不压缩
    sheet=book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)      #覆写单元格
    col=("电影链接","图片链接","影片中文名","影片外文名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,8):    #j是列数
            sheet.write(i+1,j,data[j])

    book.save(savepath)
    print("save success")

if __name__=='__main__':
    #正则表达式写在全局变量里
    findLink=re.compile(r'<a href="(.*)"')
    findImgSrc=re.compile(r'<img .* src="(.*?)"',re.S)      #re.S匹配可能出现多张图片的情况，因为re.S，所以使用懒惰匹配
    findTitle=re.compile(r'<span class="title">(.*)</span>')
    findRating=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
    findJudge=re.compile(r'<span>(\d*)人评价</span>')
    findInq=re.compile(r'<span class="inq">(.*)</span>')
    findBd=re.compile(r'<p class="">(.*?)</p>',re.S)
    main()
    