#!/usr/bin/env python3

from PIL import Image
import io

class Tileset:
    def __init__(self, json, imagedata):
        self._json = json
        self.image = Image.open(io.BytesIO(imagedata))
        self.tilewidth = json["tilewidth"]
        self.tilecount = json["tilecount"]
        self.tileheight = json["tileheight"]
        self.columns = json["columns"]
        self.name = json["name"]

    def get(self, id):
        i = id % self.columns
        j = id // self.columns
        width = self.tilewidth
        height = self.tileheight

        rect = (i * width, j * height,
                (i + 1) * width, (j + 1) * height)
        return self.image.crop(rect)


class DBMap:
    def layers(self):
        return (layer for layer in self.json["layers"])

    def object_layers(self):
        return (layer for layer in self.layers() if layer["type"] == "objectgoup")

    def tile_layers(self):
        return (layer for layer in self.layers() if layer["type"] == "tilelayer")

    def objects(self):
        return (obj for layer in self.object_layers() for obj in layer)

    def properties(self) -> list:
        return self.json["properties"]

    @staticmethod
    def property(object, name, default=None):
        return next((prop for prop in object["properties"]
                    if prop["name"] == name), default)

    def map_property(self, name, default=None):
        return next((prop for prop in self.properties()
                    if prop["name"] == name), default)

    @staticmethod
    def is_castle(object):
        return DBMap.property(object, "Type", {}).get("value") == "Castle"

    def __init__(self, image_json):
        self.json = image_json

    def validate(self):
        pass
