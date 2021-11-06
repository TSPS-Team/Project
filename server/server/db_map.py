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
    def __init__(self, image_json, entities_tileset, *tilesets):
        self._json = image_json
        self.entities_tileset = entities_tileset
        self.tilesets = [*tilesets]
