import urllib.request as req
import bs4

url1="https://www.ptt.cc/bbs/PC_Shopping/index.html"
url2="https://www.ptt.cc/bbs/MacShop/index.html"
url3="https://www.ptt.cc/bbs/e-shopping/index.html"
url4="https://www.ptt.cc/bbs/CarShop/index.html"
request1=req.Request(url1, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
})
request2=req.Request(url2, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
})
request3=req.Request(url3, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
})
request4=req.Request(url4, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
})
with req.urlopen(request1) as response:
    data1=response.read().decode("utf-8")
with req.urlopen(request2) as response:
    data2=response.read().decode("utf-8")
with req.urlopen(request3) as response:
    data3=response.read().decode("utf-8")
with req.urlopen(request4) as response:
    data4=response.read().decode("utf-8")
root1=bs4.BeautifulSoup(data1, "html.parser")
root2=bs4.BeautifulSoup(data2, "html.parser")
root3=bs4.BeautifulSoup(data3, "html.parser")
root4=bs4.BeautifulSoup(data4, "html.parser")
#爬蟲/輸出表單
#--------------------------------------------------------")
title_list1=[]
titles1=root1.find_all("div", class_="title")
for idx1, title1 in enumerate(titles1, start=1):
    if title1.a is not None:
        title_list1.append(idx1)
        title_list1_2 = f"{idx1}.{title1.a.string}"
        outlist1 = "".join([str(item) for item in title_list1_2])
        print(outlist1)
#--------------------------------------------------------")
title_list2=[]
titles2=root2.find_all("div", class_="title")
for idx2, title2 in enumerate(titles2, start=1):
    if title2.a is not None:
        title_list2.append(idx2)
        title_list2_2 = f"{idx2}. {title2.a.string}"
        outlist2 = "".join([str(item) for item in title_list2_2])
        print(outlist2)
#--------------------------------------------------------")
print("#e-shopping網購")
title_list3=[]
titles3=root3.find_all("div", class_="title")
for idx3, title3 in enumerate(titles3, start=1):
    if title3.a is not None:
        title_list3.append(idx3)
        title_list3_2 = f"{idx3}.{title3.a.string}"
        outlist3 = "".join([str(item) for item in title_list3_2])
        print(outlist3)
#--------------------------------------------------------")
print("#CarShop二手汽車")
title_list4=[]
titles4=root4.find_all("div", class_="title")
for idx4, title4 in enumerate(titles4, start=1):
    if title4.a is not None:
        title_list4.append(idx4)
        title_list4_2 = f"{idx4}.{title4.a.string}"
        outlist4 = "".join([str(item) for item in title_list4_2])
        print(outlist4)
#--------------------------------------------------------")
spans1=root1.find_all("div", class_="nrec")
spans2=root2.find_all("div", class_="nrec")
spans3=root3.find_all("div", class_="nrec")
spans4=root4.find_all("div", class_="nrec")
x1=[]
for spanx1 in spans1:
    if spanx1.span != None:
        y1 = spanx1.span.string.strip()
        try:
            x1.append(int(y1))
        except ValueError:
            x1.append(int(99))
    else:
        x1.append(0)
print(x1)
x2=[]
for spanx2 in spans2:
    if spanx2.span != None:
        y2 = spanx2.span.string.strip()
        try:
            x2.append(int(y2))
        except ValueError:
            x2.append(int(99))
    else:
        x2.append(0)
print(x2)
x3=[]
for spanx3 in spans3:
    if spanx3.span != None:
        y3 = spanx3.span.string.strip()
        try:
            x3.append(int(y3))
        except ValueError:
            x3.append(int(99))
    else:
        x3.append(0)
print(x3)
x4=[]
for spanx4 in spans4:
    if spanx4.span != None:
        y4 = spanx4.span.string.strip()
        try:
            x4.append(int(y4))
        except ValueError:
            x4.append(int(99))
    else:
        x4.append(0)
x4_str = list(map(str, x4))
x4_t = ",".join(x4_str)
print(x4_t)
print(x4)

#listx=title_list
#listy=x
#plt.bar(listx, listy, width=0.5, color='red')
#plt.title("PTT Thumbs-Up Count")
#plt.xlabel("Article ID")
#plt.ylabel("Thumbs-Up")
#plt.show()
