from flask import Flask, render_template, redirect, request, send_file, session
from util import load_image
from classes.storage import StoredImages
from classes.images import ClassImage
from PIL import Image
from io import BytesIO
import base64
import json
import os

app = Flask(__name__)
app.secret_key = "super secret key"
SAVE_PATH = "./static/images/"

def image_to_temp(image):
    image_io = BytesIO()
    image.save(image_io, "JPEG", quality=80)
    image_io.seek(0)
    return image_io

class ImageFactory:
    @staticmethod
    def create_image(_class):
        if _class == "class-1":
            image = Image.open("apple.jpeg").convert("RGB").resize((220,200))
        elif _class == "class-2":
            image = Image.open("bana.jpeg").convert("RGB").resize((220,200))
        elif _class == "class-3":
            image = Image.open("orange.jpeg").convert("RGB").resize((220,200))

        return image

@app.route("/images/", methods=["GET", "DELETE"])
def all_images():
    if request.method == "GET":
        image_list = StoredImages.get_image_list_from_directory(SAVE_PATH)

        return json.dumps({"images": [{"class":image._class, "id":image._id} for image in image_list]})

@app.route("/images/<class_id>", methods=["POST", "GET", "DELETE"])
def images(class_id):
    _class, _id = class_id.split("_")

    if request.method == "GET":
        image = StoredImages.load_image(SAVE_PATH, _class, _id).image
        image = image_to_temp(image)
        return send_file(image, mimetype="image/jpeg")

    elif request.method == "POST":
        image = ImageFactory.create_image(_class)
        _id = StoredImages.add_image(image, SAVE_PATH, _class)

        return json.dumps({"image": [{"class":_class, "id":_id}]})

    elif request.method == "DELETE":
        if _class == "ALL":
            print("ERJEJRIERIJE")
            StoredImages.delete_all(SAVE_PATH)
        else:
            StoredImages.remove_image(SAVE_PATH, _class, _id)

        return "ok"

@app.route("/", methods=["GET"])
def weight_imprinting_demo():
    return render_template("weightImprintingDemo.html")

if __name__ == "__main__":
    app.run(debug=True)
