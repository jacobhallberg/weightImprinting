from PIL import Image
from classes.storage import StoredImages
from io import BytesIO
import base64

def load_image(_class,_id, save_path):
    image_io = BytesIO()
    temp_image = Image.open(save_path + "{}_{}.jpeg".format(_class,_id))
    temp_image.save(image_io, "JPEG", quality=80)
    image_io.seek(0)

    return image_io
