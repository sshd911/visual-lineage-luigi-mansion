from flask import Flask, render_template, Response
from controllers.index import IndexController
from numba import jit

app = Flask(__name__)
app.config["DEBUG"] = False
app.config["HOST"] = "0.0.0.0"
app.config["PORT"] = 80


@app.route("/video_feed")
def video_feed():
    return Response(IndexController().index(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host=app.config["HOST"], port=app.config["PORT"])
