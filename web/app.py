from flask import Flask, render_template, Response
from web.controllers.index import IndexController
import sys
import os

WEB_DIR = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), "web")
sys.path.append(WEB_DIR)

app = Flask(__name__)
app.config["DEBUG"] = False
app.config["HOST"] = "127.0.0.1"
app.config["PORT"] = 80


@app.route("/video_feed")
def video_feed():
    return Response(IndexController().index(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host=app.config["HOST"], port=app.config["PORT"])
