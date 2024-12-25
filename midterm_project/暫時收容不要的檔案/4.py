import urllib.request as req
import bs4
import matplotlib.pyplot as plt

#e-shopping網購
url="https://www.ptt.cc/bbs/e-shopping/index.html"
request=req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
    
root=bs4.BeautifulSoup(data, "html.parser")

#爬蟲/輸出表單
title_list=[]
titles=root.find_all("div", class_="title")
for idx, title in enumerate(titles, start=1):
    if title.a is not None:
        title_list.append(idx)
        print(f"{idx}. {title.a.string}")

spans=root.find_all("div", class_="nrec")
x=[]
for spanx in spans:
    if spanx.span != None:
        y = spanx.span.string.strip()
        try:
            x.append(int(y))
        except ValueError:
            x.append(int(99))
    else:
        x.append(0)
print(x)

listx=title_list
listy=x
plt.bar(listx, listy, width=0.5, color='red')
plt.title("PTT Thumbs-Up Count")
plt.xlabel("Article ID")
plt.ylabel("Thumbs-Up")
plt.show()
