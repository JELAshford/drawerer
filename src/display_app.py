"""Send numpy arrays from a "Simulation" to local webpage for visualisation"""

from flask import Flask, render_template, Response
from io import BytesIO
from PIL import Image
import numpy as np
import time


class Simulation:
    def __init__(self, target_fps=60):
        self.img_buffer = BytesIO()
        self.target_fps = target_fps

    def step(self) -> np.ndarray:
        raise NotImplementedError()

    def emit_jpeg(self):
        for output_array in self.step():
            img = Image.fromarray(output_array, "RGB")
            self.img_buffer.seek(0)
            self.img_buffer.truncate()
            img.save(self.img_buffer, format="JPEG")
            self.img_buffer.seek(0)
            yield (
                b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                + self.img_buffer.read()
                + b"\r\n"
            )
            # TODO; Use time differences to make this accurate
            time.sleep(1 / self.target_fps)


class DisplayApp:
    def __init__(
        self,
        simulation_instance: Simulation,
        host: str = "0.0.0.0",
        port: int = 8080,
        debug: bool = True,
    ):
        self.simulation_instance = simulation_instance
        self.app_params = dict(host=host, port=port, debug=debug)
        self.app = Flask(__name__, template_folder="./")

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/video_feed")
        def video_feed():
            return Response(
                self.simulation_instance.emit_jpeg(),
                mimetype="multipart/x-mixed-replace; boundary=frame",
            )

    def run(self):
        self.setup_routes()
        self.app.run(**self.app_params)
