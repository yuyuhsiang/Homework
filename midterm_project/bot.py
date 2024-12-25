from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import urllib.request as req
import bs4, requests, json, time, statistics

url1="https://www.ptt.cc/bbs/PC_Shopping/index.html"
url2="https://www.ptt.cc/bbs/MacShop/index.html"
url3="https://www.ptt.cc/bbs/nb-shopping/index.html"
url4="https://www.ptt.cc/bbs/e-shopping/index.html"
request1=req.Request(url1, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"})
request2=req.Request(url2, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"})
request3=req.Request(url3, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"})
request4=req.Request(url4, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"})
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
title_list1=[]
titles1=root1.find_all("div", class_="title")
outlist1 = []
for idx1, title1 in enumerate(titles1, start=1):
    if title1.a is not None:
        title_list1.append(idx1)
        title_list1_2 = f"{idx1}.{title1.a.string}"
        outlist1.append(title_list1_2)
        outlist1_str = "\n".join(outlist1)
title_list2=[]
titles2=root2.find_all("div", class_="title")
outlist2 = []
for idx2, title2 in enumerate(titles2, start=1):
    if title2.a is not None:
        title_list2.append(idx2)
        title_list2_2 = f"{idx2}. {title2.a.string}"
        outlist2.append(title_list2_2)
        outlist2_str = "\n".join(outlist2)
title_list3=[]
titles3=root3.find_all("div", class_="title")
outlist3 = []
for idx3, title3 in enumerate(titles3, start=1):
    if title3.a is not None:
        title_list3.append(idx3)
        title_list3_2 = f"{idx3}.{title3.a.string}"
        outlist3.append(title_list3_2)
        outlist3_str = "\n".join(outlist3)
title_list4=[]
titles4=root4.find_all("div", class_="title")
outlist4 = []
for idx4, title4 in enumerate(titles4, start=1):
    if title4.a is not None:
        title_list4.append(idx4)
        title_list4_2 = f"{idx4}.{title4.a.string}"
        outlist4.append(title_list4_2)
        outlist4_str = "\n".join(outlist4)
spans1=root1.find_all("div", class_="nrec")
spans2=root2.find_all("div", class_="nrec")
spans3=root3.find_all("div", class_="nrec")
spans4=root4.find_all("div", class_="nrec")
x1 = []
for index, spanx1 in enumerate(spans1, start=1):
    if spanx1.span is not None:
        y1 = spanx1.span.string.strip()
        try:
            x1.append(int(y1))
        except ValueError:
            x1.append(int(99))
    else:
        x1.append(0)
x1_str = [f"{index}_{value}" for index, value in enumerate(x1, start=1)]
x1_t = ",".join(x1_str)
x1append = x1_t
x2 = []
for index, spanx2 in enumerate(spans2, start=1):
    if spanx2.span is not None:
        y2 = spanx2.span.string.strip()
        try:
            x2.append(int(y2))
        except ValueError:
            x2.append(int(99))
    else:
        x2.append(0)
x2_str = [f"{index}_{value}" for index, value in enumerate(x2, start=1)]
x2_t = ",".join(x2_str)
x2append = x2_t
x3 = []
for index, spanx3 in enumerate(spans3, start=1):
    if spanx3.span is not None:
        y3 = spanx3.span.string.strip()
        try:
            x3.append(int(y3))
        except ValueError:
            x3.append(int(99))
    else:
        x3.append(0)
x3_str = [f"{index}_{value}" for index, value in enumerate(x3, start=1)]
x3_t = ",".join(x3_str)
x3append = x3_t
x4 = []
for index, spanx4 in enumerate(spans4, start=1):
    if spanx4.span is not None:
        y4 = spanx4.span.string.strip()
        try:
            x4.append(int(y4))
        except ValueError:
            x4.append(int(99))
    else:
        x4.append(0)
x4_str = [f"{index}_{value}" for index, value in enumerate(x4, start=1)]
x4_t = ",".join(x4_str)
x4append = x4_t


app = Flask(__name__)
handler = WebhookHandler("00962e96a4335cb82a8d06285be21b4a")
line_bot_api = LineBotApi("MuIWSmEPGBeYD55cP0zR2XlZAqJFxhJ3QmT4+EWq5WXPCIugwC9dzhRbLxWjrrhSBos0vpbJ23r3cVKus9ILHxvSbPtxJ+dQc8T2fMuAEvfImEkDvFYa2G0Aa+Uq2Gwym0EQ3MuS55vUFrAbBFPE4wdB04t89/1O/w1cDnyilFU=")

json_url = "https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON"

def search_by_sitename(sitename):
    try:
        response = requests.get(json_url)
        response.raise_for_status()
        data = response.json()

        filtered_records = [record for record in data['records'] if record['sitename'] == sitename]

        if filtered_records:
            response_message = ""
            for record in filtered_records:
                response_message += f"測站: {record['sitename']}\n所在縣市: {record['county']}\nAQI: {record['aqi']}\n空氣狀況: {record['status']}\n偵測時間: \n{record['publishtime']}\n------------------------\n"
        else:
            response_message = f"No records found for sitename: {sitename}"

        return response_message

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"

def get_image_url_from_json():
    json_data2 = {
 "cwaopendata": {
  "@xmlns": "urn:cwa:gov:tw:cwacommon:0.1",
  "identifier": "25fcee18-ac9e-11ee-ab31-2c44fd85440d",
  "sender": "od@cwa.gov.tw",
  "sent": "2024-01-06T22:16:13+08:00",
  "status": "Actual",
  "msgType": "Issue",
  "dataid": "O-A0038-001",
  "scope": "Public",
  "dataset": {
   "datasetinfo": {
    "datasetDescription": "地理資訊",
    "parameterset": [
     {
      "parameterName": "經度範圍",
      "parameterValue": "119.188 - 123.588"
     },
     {
      "parameterName": "緯度範圍",
      "parameterValue": "21.523 - 25.938"
     }
    ]
   },
   "time": {
    "obsTime": "2024-01-06T22:00:00+08:00"
   },
   "resource": {
    "resourceDesc": "溫度分布圖",
    "mimeType": "image/jpeg",
    "uri": "https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-A0038-001.jpg"
   }
  }
 }
}
    image_uri2 = json_data2['cwaopendata']['dataset']['resource']['uri']
    return image_uri2


@app.route("/callback", methods = ["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if isinstance(event.message, TextMessage):
        msg = event.message.text
        if msg == "電腦二手":
            txt1 = "熱門程度:\n" + x1append+ "\n文章列表:\n" + outlist1_str
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = txt1))
        if msg == "蘋果二手":
            txt2 = "熱門程度:\n" + x2append+ "\n文章列表:\n" + outlist2_str
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = txt2))
        if msg == "筆電二手":
            txt3 = "熱門程度:\n" + x3append+ "\n文章列表:\n" + outlist3_str
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = txt3))
        if msg == "網購":
            txt4 = "熱門程度:\n" + x4append+ "\n文章列表:\n" + outlist4_str
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = txt4))
        elif "溫度" in msg:
            image_url2 = get_image_url_from_json()
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=image_url2, preview_image_url=image_url2))
        else:
            user_message = event.message.text
            response_message = search_by_sitename(user_message)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))

if __name__ == "__main__":
    app.run(port=5000)
