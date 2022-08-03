#!/usr/bin/python
import cv2
import numpy
from flask import Flask, Response, request

app = Flask(__name__)


@app.route("/infer", methods=["POST"])
def predict_image():
    return Response(request.get_data())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
