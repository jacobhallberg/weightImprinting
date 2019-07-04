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

def load_image_session():
    if "images" not in session:
        session["images"] = ""
        stored_images = StoredImages(SAVE_PATH) 
    else:
        stored_images = StoredImages(SAVE_PATH, session["images"])

    return stored_images

class ImageFactory:
    def __init__(self, _class):
        if _class == "class-1":
            image = Image.open("apple.jpeg").convert("RGB").resize((220,200))
        elif _class == "class-2":
            image = Image.open("bana.jpeg").convert("RGB").resize((220,200))
        elif _class == "class-3":
            image = Image.open("orange.jpeg").convert("RGB").resize((220,200))

        self.image = image

@app.route("/images/", methods=["GET"])
def all_images():
    stored_images = load_image_session()
    
    session["images"] = ""

    if request.method == "GET":
        stored_images = load_image_session()
        image_list = stored_images.get_image_list()

        return json.dumps({"images": [{"class":image._class, "id":image.save_path.split("/")[-1].split(".")[0].split("_")[-1]} for image in image_list]})

@app.route("/images/<class_id>", methods=["POST", "GET", "DELETE"])
def images(class_id):
    _class, _id = class_id.split("_")
    stored_images = load_image_session()

    if request.method == "GET":
        stored_images = load_image_session()
        image_list = stored_images.get_image_list()
        
        image = load_image(_class, _id, SAVE_PATH)
        return send_file(image, mimetype="image/jpeg")

    elif request.method == "POST":
        factory = ImageFactory(_class)
        image = factory.image 

        stored_images.add_image(image, _class)
        session["images"] = str(stored_images)

        return json.dumps({"image": [{"class":_class, "id":stored_images._id}]})

    elif request.method == "DELETE":
        if _class == "ALL":
            session["images"] = StoredImages(SAVE_PATH)
        else:
            stored_images.remove_image(_class, _id)
            session["images"] = str(stored_images)

        return "ok"

@app.route("/", methods=["GET"])
def weight_imprinting_demo():
    return render_template("weightImprintingDemo.html")

if __name__ == "__main__":
    app.run(debug=True)
