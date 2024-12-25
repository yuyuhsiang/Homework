import cv2
import os, glob
import numpy as np
from time import sleep

def saveImg(image, index): #圖片存檔
    filename = 'images/' + name + '/face{:03d}.jpg'.format(index)
    cv2.imwrite(filename, image)
    
index = 1
total = 100 #人臉取樣總數

name = input('輸入姓名(使用英文)：')
if os.path.isdir('images/' + name): #使用姓名作為資料夾名稱
    print('此姓名已存在！')
else:
    os.mkdir('images/' + name) #建立資料夾
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    cap = cv2.VideoCapture(0) #開啟攝影機
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    while index > 0: #取樣
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) #框選臉部
            image = cv2.resize(gray[y: y + h, x: x + w], (400, 400)) #存檔圖片大小
            saveImg(image, index)
            sleep(0.1)
            index += 1
            if index > total:
                print('取樣完成！')
                index = -1 #離開迴圈
                break
        cv2.imshow('video', frame)
        cv2.waitKey(1)
    cap.release() #關閉cam
    cv2.destroyAllWindows()
    
images = [] #存所有訓練圖形
labels = [] #存所有訓練標籤
labelstr = [] #會員姓名
count = 0 #會員編號索引
dirs = os.listdir('images') #取得所有資料夾及檔案
for d in dirs:
    if os.path.isdir('images/' + d): #只處理資料表
        files = glob.glob('images/' + d + '/*.jpg') #取得資料夾中所有圖檔
        for filename in files: #逐一處理圖片
            img = cv2.imread(filename, cv2.COLOR_BGR2GRAY)
            images.append(img)
            labels.append(count) #以數值作為標籤
        labelstr.append(d) #將姓名加入串列
        count += 1
        
#建立姓名檔案，在辨識人臉時使用
f = open('member.txt', 'w')
f.write(','.join(labelstr))
f.close()

print('開始建立模型...')
model = cv2.face.LBPHFaceRecognizer_create() #建立LBPH空模型
model.train(np.asarray(images), np.asarray(labels)) #訓練模型
model.save('faces_LBPH.yml') #儲存模型
print('建立模型完成！')