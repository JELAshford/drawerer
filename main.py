"""Basic array sending to a local webpage
based off: https://github.com/abishekparajuli-np/flask-opencv-webcam-stream
I've cut out a lot of the interface functinoality, might want that back for
interactive elements/reloading?"""

from flask import Flask, render_template, Response
from io import BytesIO
from PIL import Image
import numpy as np
import time

app = Flask(__name__, template_folder="./")
rng = np.random.default_rng()
img_buffer = BytesIO()


def generate_frames():
    global rng, img_buffer
    while True:
        # based on https://stackoverflow.com/a/70275120
        array = rng.integers(0, 255, size=(200, 200, 3), dtype=np.uint8)
        img = Image.fromarray(array, "RGB")
        img_buffer.seek(0)
        img_buffer.truncate()
        img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)
        yield (
            b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + img_buffer.read() + b"\r\n"
        )
        time.sleep(1 / 60)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
