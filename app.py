import argparse
import io
import os
from PIL import Image

import torch
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        file = request.files["file"]
        print(file)
        img_bytes = file.read()
        print(img_bytes)
        img = Image.open(io.BytesIO(img_bytes))
        results = model([img])
@app.route('/<path:filename>')
def display(filename):
    detection_path = "yolov5/runs/detect/"
    all_dir = [folder for folder in os.listdir(os.path.join(detection_path))]
    print(all_dir)
    latest_dir = max(all_dir, key=lambda x: os.path.getctime(os.path.join(detection_path, x)))
    print(latest_dir)
    latest_dir_path=detection_path+"/"+latest_dir
    latest_file = os.listdir(os.path.join(latest_dir_path))[0]
    print(latest_file)
    full_file_path=latest_dir_path+"/"+latest_file
    print(full_file_path)
    environment= request.environ
    return send_from_directory(latest_dir_path,latest_dir)


        results.render()  # updates results.imgs with boxes and labels
        results.save(save_dir="static/")
        return redirect("static/image0.jpg")

    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # force_reload = recache latest code
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat