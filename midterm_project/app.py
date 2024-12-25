from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
import os
import time
from datetime import datetime

app = Flask(__name__)

# 設定存儲路徑
UPLOAD_FOLDER = 'static/images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 載入人臉分類器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

# 全局變數
camera = None
is_capturing = False
capture_count = 0
current_name = None

def init_model():
    """初始化人臉辨識模型"""
    model = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists('faces_LBPH.yml'):
        model.read('faces_LBPH.yml')
    return model

def save_member_names(names):
    """保存會員名單"""
    with open('member.txt', 'w', encoding='utf-8') as f:
        f.write(','.join(names))

def load_member_names():
    """載入會員名單"""
    if os.path.exists('member.txt'):
        with open('member.txt', 'r', encoding='utf-8') as f:
            return f.readline().strip().split(',')
    return []

def train_model():
    """訓練模型"""
    images = []
    labels = []
    label_names = []
    label_idx = 0
    
    # 遍歷所有會員資料夾
    for name in os.listdir(UPLOAD_FOLDER):
        if os.path.isdir(os.path.join(UPLOAD_FOLDER, name)):
            member_path = os.path.join(UPLOAD_FOLDER, name)
            for img_file in os.listdir(member_path):
                if img_file.endswith('.jpg'):
                    img_path = os.path.join(member_path, img_file)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        images.append(img)
                        labels.append(label_idx)
            label_names.append(name)
            label_idx += 1
    
    if images:
        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(np.array(images), np.array(labels))
        model.save('faces_LBPH.yml')
        save_member_names(label_names)
        return True
    return False

def generate_frames():
    """生成視頻流"""
    global camera, is_capturing, capture_count, current_name
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # 翻轉畫面
        frame = cv2.flip(frame, 1)
        
        # 轉換成灰度圖
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)
        
        for (x, y, w, h) in faces:
            # 畫框
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            if is_capturing and current_name:
                # 儲存人臉圖片
                face_img = cv2.resize(gray[y:y+h, x:x+w], (400, 400))
                img_path = os.path.join(UPLOAD_FOLDER, current_name, f'face_{capture_count:03d}.jpg')
                cv2.imwrite(img_path, face_img)
                capture_count += 1
                time.sleep(0.1)
                
                if capture_count >= 100:  # 收集100張照片後停止
                    is_capturing = False
                    capture_count = 0
                    current_name = None
                    train_model()  # 重新訓練模型
        
        # 添加計數器顯示
        if is_capturing:
            cv2.putText(frame, f'Capturing: {capture_count}/100', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """首頁"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """視頻流端點"""
    return Response(generate_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    """開始擷取人臉"""
    global camera, is_capturing, capture_count, current_name
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'success': False, 'message': '請輸入姓名'})
    
    # 建立用戶資料夾
    user_folder = os.path.join(UPLOAD_FOLDER, name)
    if os.path.exists(user_folder):
        return jsonify({'success': False, 'message': '此用戶名已存在'})
    
    os.makedirs(user_folder)
    current_name = name
    is_capturing = True
    capture_count = 0
    
    return jsonify({'success': True})

@app.route('/verify_face', methods=['POST'])
def verify_face():
    """驗證人臉"""
    global camera
    
    if camera is None:
        return jsonify({'success': False, 'message': '相機未開啟'})
    
    # 捕獲一幀
    ret, frame = camera.read()
    if not ret:
        return jsonify({'success': False, 'message': '無法捕獲影像'})
    
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    
    if len(faces) == 0:
        return jsonify({'success': False, 'message': '未偵測到人臉'})
    
    model = init_model()
    names = load_member_names()
    
    if not names:
        return jsonify({'success': False, 'message': '尚未有註冊會員'})
    
    # 對每個偵測到的人臉進行辨識
    for (x, y, w, h) in faces:
        face_img = cv2.resize(gray[y:y+h, x:x+w], (400, 400))
        try:
            label, confidence = model.predict(face_img)
            if confidence < 50:  # 置信度閾值
                return jsonify({
                    'success': True,
                    'name': names[label],
                    'confidence': float(confidence)
                })
            else:
                return jsonify({'success': False, 'message': '無法辨識此人臉'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'辨識錯誤: {str(e)}'})
    
    return jsonify({'success': False, 'message': '辨識失敗'})

@app.route('/init_camera')
def init_camera():
    """初始化相機"""
    global camera
    
    if camera is None:
        camera = cv2.VideoCapture(0)
    return jsonify({'success': True})

@app.route('/release_camera')
def release_camera():
    """釋放相機"""
    global camera
    
    if camera is not None:
        camera.release()
        camera = None
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)