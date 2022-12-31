from flask import Flask, render_template, Response
from cvzone.HandTrackingModule import HandDetector
from game import Game
import numpy as np
import cv2

app = Flask(__name__)
app.config['debug'] = False
app.config['host'] = "0.0.0.0"
app.config['port'] = 80

def init():
    game = Game()
    cap = cv2.VideoCapture(-1)
    dw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    dh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    if cap.isOpened():
        while True:
            _, img = cap.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False)
            # bg_img = np.zeros((dh, dw, 3), np.uint8)
            if hands:
                lmList = hands[0]["lmList"]
                pointIndex = lmList[8][0:2]
                img = game.update(img, pointIndex, dh, dw, cap)
                # bg_img = game.update(bg_img, pointIndex, dh, dw, cap)
            _, buffer = cv2.imencode(".jpg", img)
            # _, buffer = cv2.imencode(".jpg", bg_img)
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(init(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=app.config['debug'], host=app.config['host'], port=app.config['port'])
