from PIL import Image
from classes.images import ClassImage
import os
import uuid
from glob import glob

class StoredImages:
    def __init__(self, save_path, load_from_directory=True):
        self.images = {}
        self.save_path = save_path
       
        if load_from_directory: 
            self.images = StoredImages.get_paths_from_directory()

    @staticmethod
    def remove_image(save_path, _class, _id):
        image = save_path + "{}_{}.jpeg".format(_class, _id)
        os.remove(image)

    @staticmethod
    def add_image(image, save_path, _class):
        _id = str(uuid.uuid1())
        image_path = save_path + "{}_{}.jpeg".format(_class, _id)
        image.save(image_path)
        image = image_path

        return _id

    @staticmethod 
    def get_image_list_from_directory(directory):
        class_image_list = []
        for image_path in glob(directory + "*"):
            _class, _id = image_path.split("/")[-1].split(".")[0].split("_")
            class_image_list.append(StoredImages.load_image(directory, _class, _id))

        return class_image_list

    @staticmethod
    def get_paths_from_directory(directory):
        class_image_dictionary = {}
        for image_path in glob(directory + "*"):
            _class, _id = image_path.split("/")[-1].split(".")[0].split("_")

            class_image_dictionary = StoredImages.add_image_to_dictionary(class_image_dictionary, _class, _id, image_path)

        return class_image_dictionary

    @staticmethod
    def get_image_dictionary_from_directory(directory):
        class_image_dictionary = {}
        for image_path in glob(directory + "*"):
            _class, _id = image_path.split("/")[-1].split(".")[0].split("_")
            image = StoredImages.load_image(directory, _class, _id)

            class_image_dictionary = StoredImages.add_image_to_dictionary(class_image_dictionary, _class, _id, image)

        return class_image_dictionary
    
    @staticmethod
    def add_image_to_dictionary(dictionary, _class, _id, image):
        if _class in dictionary:
            dictionary[_class].append(image)
        else:
            dictionary[_class] = [image]

        return dictionary

    @staticmethod
    def delete_all(save_path):
        for image_path in glob(save_path + "*"):
            os.remove(image_path)
    
    @staticmethod 
    def load_image(save_path, _class, _id):
        image = Image.open(save_path + _class + "_" + _id + ".jpeg").convert("RGB").resize((220,220))
        image = ClassImage(image, save_path, _class, _id)
        return image
