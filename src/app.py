from flask import Flask, render_template, Response
from cvzone.HandTrackingModule import HandDetector
from main import Main
import numpy as np
import cv2
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
game = Main(f"{base_dir}/static/fly.png")
app = Flask(__name__)
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
dw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
dh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def init():
    while True:
        _, img = cap.read()
        bg = np.zeros((dh, dw, 3), np.uint8)
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        if hands:
            lmList = hands[0]["lmList"]
            pointIndex = lmList[8][0:2]
            bg = game.update(bg, pointIndex, dh, dw)
        _, buffer = cv2.imencode(".jpg", bg)
        frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(init(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
