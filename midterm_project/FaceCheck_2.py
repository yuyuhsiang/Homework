from flask import Flask, render_template, Response, request, jsonify
import cv2
import os
import numpy as np
from time import sleep

app = Flask(__name__)

class FaceRecognition:
    def __init__(self):
        self.camera = None
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
        self.current_name = ""
        self.index = 1
        self.total = 100
        self.is_training = False
        self.is_recognizing = False
        self.model = None
        self.names = []
        self.recognized_name = None

    def save_img(self, image, index):
        """Save captured face image to the corresponding folder"""
        if self.current_name:
            filename = f'images/{self.current_name}/{index}.jpg'
            cv2.imwrite(filename, image)

    def gen_frames(self, mode='train'):
        self.camera = cv2.VideoCapture(0)
        while True:
            success, frame = self.camera.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 3)
            
            if mode == 'train' and self.is_training:
                for (x, y, w, h) in faces:
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    if self.current_name and self.index <= self.total:
                        image = cv2.resize(gray[y:y+h, x:x+w], (400, 400))
                        self.save_img(image, self.index)
                        self.index += 1
                        sleep(0.1)
                        if self.index > self.total:
                            self.is_training = False
                            self.train_model()
            
            elif mode == 'recognize' and self.is_recognizing:
                for (x, y, w, h) in faces:
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    face_img = cv2.resize(gray[y:y+h, x:x+w], (400, 400))
                    try:
                        if self.model is None:
                            self.load_model()
                        val = self.model.predict(face_img)
                        if val[1] < 50:
                            name = self.names[val[0]]
                            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            self.recognized_name = name
                            self.is_recognizing = False
                    except Exception as e:
                        print(f"Recognition error: {e}")

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    def train_model(self):
        images = []
        labels = []
        labelstr = []
        count = 0
        
        dirs = os.listdir('images')
        for d in dirs:
            if os.path.isdir(f'images/{d}'):
                for filename in os.listdir(f'images/{d}'):
                    if filename.endswith('.jpg'):
                        img_path = f'images/{d}/{filename}'
                        img = cv2.imread(img_path, cv2.COLOR_BGR2GRAY)
                        images.append(img)
                        labels.append(count)
                labelstr.append(d)
                count += 1

        with open('member.txt', 'w') as f:
            f.write(','.join(labelstr))

        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.model.train(np.asarray(images), np.asarray(labels))
        self.model.save('faces_LBPH.yml')
        self.names = labelstr
        return True

    def load_model(self):
        if os.path.exists('faces_LBPH.yml'):
            self.model = cv2.face.LBPHFaceRecognizer_create()
            self.model.read('faces_LBPH.yml')
            with open('member.txt', 'r') as f:
                self.names = f.readline().split(',')
            return True
        return False

face_rec = FaceRecognition()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognition')
def recognition():
    return render_template('recognition.html')

@app.route('/video_feed_train')
def video_feed_train():
    return Response(face_rec.gen_frames('train'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_recognize')
def video_feed_recognize():
    return Response(face_rec.gen_frames('recognize'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    name = request.form.get('name')
    if not name:
        return {"status": "error", "message": "請輸入姓名"}
    
    if os.path.isdir(f'images/{name}'):
        return {"status": "error", "message": "此姓名已存在"}
    
    os.makedirs(f'images/{name}')
    face_rec.current_name = name
    face_rec.index = 1
    face_rec.is_training = True
    return {"status": "success"}

@app.route('/start_recognition', methods=['POST'])
def start_recognition():
    face_rec.is_recognizing = True
    return {"status": "success"}

@app.route('/recognition_result')
def recognition_result():
    if face_rec.recognized_name:
        result = {'status': 'success', 'name': face_rec.recognized_name}
        face_rec.recognized_name = None
        return jsonify(result)
    return jsonify({'status': 'pending'})

if __name__ == '__main__':
    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)