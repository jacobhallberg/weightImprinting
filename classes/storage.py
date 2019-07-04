from PIL import Image
from classes.images import ClassImage
import os

class StoredImages:
    def __init__(self, save_path, stored_image_dict=None):
        self.images = {}
        self.save_path = save_path
        self._id = 0

        if stored_image_dict is not None and len(stored_image_dict) > 0: self.from_dict(stored_image_dict)

    def add_image(self, image, _class):
        image_path = self.save_path + "{}_{}.jpeg".format(_class, self.image_id())
        image.save(image_path)
        image = image_path

        if _class in self.images:
            self.images[_class].append(image)
        else:
            self.images[_class] = [image]

    def remove_image(self, _class, _id):
        image = self.save_path + "{}_{}.jpeg".format(_class, _id)
        if _class in self.images:
            self.images[_class].pop(self.images[_class].index(image))
            os.remove(image)
            if len(self.images[_class]) == 0:
                self.images.pop(_class, None)
        else:
            print("Image not found.")

    def image_id(self):
        self._id += 1

        return self._id

    def get_image_list(self):
        class_image_list = []
        for _class, image_paths in self.images.items():
            class_image_list += [ClassImage(Image.open(image_path).convert("RGB"), _class, image_path) for image_path in image_paths]
        return class_image_list

    def get_images(self):
        class_image_dictionary = {}
        for _class, image_paths in self.images:
            class_image_dictionary[_class] = [ClassImage(Image.open(image_path).convert("RGB"), _class, image_path) for image_path in image_paths]
        return class_image_dictionary

    def from_dict(self, string_dictionary):
        for class_data in string_dictionary.split("|"):
            _class, image_paths = class_data.split(":")
            image_paths = image_paths.split(",")
            
            if self._id <= max([int(image_path.split("_")[1][0]) for image_path in image_paths]): self._id = max([int(image_path.split("_")[1][0]) for image_path in image_paths]) + 1
            self.images[_class] = [image_path for image_path in image_paths]

    def __str__(self):
        stored_images = ""
        for _class, image_paths in self.images.items():
            stored_images += "{}:{},".format(_class, ",".join(image_paths))
            stored_images = stored_images[:-1] + "|"

        stored_images = stored_images[:-1]
        return stored_images
