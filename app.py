from flask import Flask, render_template, Response
from cvzone.HandTrackingModule import HandDetector
from main import Main
import cv2

app = Flask(__name__)


def init():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    game = Main("Donut.png")
    while True:
        _, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            lmList = hands[0]["lmList"]
            pointIndex = lmList[8][0:2]
            img = game.update(img, pointIndex)
        _, buffer = cv2.imencode(".jpg", img)
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
