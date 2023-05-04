import os
from flask import Flask,render_template,request,jsonify,send_from_directory
app = Flask(__name__)
import shutil


@app.route('/',methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/", methods=['GET','POST'])
def predict_img():
    if request.method == 'POST':
      if 'file' in request.files:
         f= request.files['file']
         file_path=os.path.join(os.getcwd(),'static','input_images',f.filename)
         image_name=f.filename
         f.save(file_path)
         print(image_name)
         print(file_path)
         os.system("python yolov5/detect.py --weights best.pt --img 416 --conf 0.1 --source static/input_images/{name}".format(name=image_name))
         return display_predicted_image()

@app.route('/display')
def display_predicted_image():
    detection_path = "yolov5/runs/detect/"
    all_dir = [folder for folder in os.listdir(os.path.join(detection_path))]
    print(all_dir)
    latest_dir = max(all_dir, key=lambda x: os.path.getctime(os.path.join(detection_path, x)))
    print(latest_dir)
    latest_dir_path = detection_path + '/' + latest_dir
    print(latest_dir_path)
    image = os.listdir(os.path.join(latest_dir_path))[0]
    print(image)
    detected_image_path = latest_dir_path + '/' + image
    print(detected_image_path)
    shutil.copy(detected_image_path,'static/predicted_images/')

    return render_template("display.html", image_filename=image)



@app.route('/live',methods=['GET'])
def predict_live():
    os.system("python yolov5/detect.py --weights best.pt --img 416 --conf 0.2 --source 0")
    return "Camera starting!!"

if __name__ == "__main__":
    app.run(debug=True)