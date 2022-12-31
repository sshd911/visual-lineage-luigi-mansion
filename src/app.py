from flask import Flask, render_template, Response
from cvzone.HandTrackingModule import HandDetector
from main import Main
# from main import Main
import numpy as np
import cv2

app = Flask(__name__)

def init():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    dw, dh = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    while True:
        _, img = cap.read()
        # bg = np.zeros((dh, dw, 3), np.uint8)
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        if hands:
            lmList = hands[0]["lmList"]
            pointIndex = lmList[8][0:2]
            img = game.update(img, pointIndex, dh, dw)
        _, buffer = cv2.imencode(".jpg", img)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
        )


@app.route("/video_feed")
def video_feed():
    return Response(init(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    game = Main()
    app.run(port=80)
