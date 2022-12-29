from flask import Flask, render_template, Response
import mediapipe as mp
import numpy as np
import cv2

app = Flask(__name__)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def gen_frames(mpHands, hands, mpDraw):
    cap = cv2.VideoCapture(0)
    while True:
        gray_img = np.zeros((1000, 1000, 3), np.uint8)
        suzccess, img = cap.read()
        if not suzccess:
            break
        else:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            if results.multi_hand_landmarks:
                for handlms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handlms.landmark):
                        h, w, c = imgRGB.shape
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        if id in [10, 11, 12]:
                            cv2.circle(imgRGB, (cx, cy), 15, (139, 0, 0), cv2.FILLED)
                    mpDraw.draw_landmarks(gray_img, handlms, mpHands.HAND_CONNECTIONS)
            _, buffer = cv2.imencode('.jpg', gray_img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(mpHands, hands, mpDraw), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)