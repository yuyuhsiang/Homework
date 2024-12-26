from flask import Flask, render_template, Response, request
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

    def save_img(self, image, index):
        filename = f'images/{self.current_name}/face{index:03d}.jpg'
        cv2.imwrite(filename, image)

    def gen_frames(self):
        self.camera = cv2.VideoCapture(0)
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            else:
                frame = cv2.flip(frame, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 3)
                
                for (x, y, w, h) in faces:
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    if self.current_name and self.index <= self.total:
                        image = cv2.resize(gray[y:y+h, x:x+w], (400, 400))
                        self.save_img(image, self.index)
                        self.index += 1
                        sleep(0.1)

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

        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(np.asarray(images), np.asarray(labels))
        model.save('faces_LBPH.yml')
        return True

face_rec = FaceRecognition()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(face_rec.gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    name = request.form.get('name')
    if not name:
        return {"status": "error", "message": "Name is required"}
    
    if os.path.isdir(f'images/{name}'):
        return {"status": "error", "message": "Name already exists"}
    
    os.makedirs(f'images/{name}')
    face_rec.current_name = name
    face_rec.index = 1
    return {"status": "success"}

@app.route('/train', methods=['POST'])
def train():
    try:
        face_rec.train_model()
        return {"status": "success", "message": "Model trained successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    if not os.path.exists('images'):
        os.makedirs('images')
    app.run(debug=True)