import numpy as np
import requests
import base64


with open("apple.jpeg", "rb") as image:
    image = base64.b64encode(image.read())


form_data = { 
        "image": ("", image),
        "class": ("", "Apple") 
        }

response = requests.post("http://localhost:5000/images/", files=form_data)

