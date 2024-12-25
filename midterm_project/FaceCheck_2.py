import cv2
import time
import PIL as Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

model = cv2.face.LBPHFaceRecognizer_create()
model.read('faces_LBPH.yml')
f = open('member.txt', 'r') #讀入模型
names = f.readline().split(',') #讀入姓名存於串列

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
cap = cv2.VideoCapture(0)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

timenow = time.time() #取得現在時間數值
while(cap.isOpened()): #cam開啟成功
    count = 2 - int(time.time() - timenow) #倒數計時5秒
    ret, img = cap.read()
    if ret == True:
        imgcopy = img.copy() #複製影像
        cv2.putText(imgcopy, str(count), (200,400), cv2.FONT_HERSHEY_SIMPLEX, 15, (0,0,255), 35) #在複製影像上畫倒數秒數
        cv2.imshow("frame", imgcopy) #顯示複製影像
        k = cv2.waitKey(100) #0.1秒讀鍵盤一次
        if k == ord("z") or k == ord("Z") or count == 0: #按Z鍵或倒數計時結束
            cv2.imwrite("media/tem.jpg", img) #將影像存檔
            break
cap.release() #關閉cam
cv2.destroyAllWindows()

img = cv2.imread("media/tem.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 3)
for (x, y, w, h) in faces:
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    face_img = cv2.resize(gray[y: y + h, x: x + w], (400, 400)) #調整成訓練時大小
    try:
        val = model.predict(face_img)
        if val[1] <50: #辨識成功，顯示登入訊息
            print('歡迎' + names[val[0]] + '登入！(請掃描QRcode以加入LineBOT)')
            APIimage_path = "LineDevelopAPI.png"
            APIimage = mpimg.imread(APIimage_path)
            imgplot = plt.imshow(APIimage)
            plt.show()
        else:
            print('抱歉！你不是會員，請你離開！')
    except:
        print('辨識時產生錯誤！')
