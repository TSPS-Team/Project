#!/usr/bin/env python3

class Tileset:
    def __init__(self, json, imagedata):
        self._json = json
        self.imagedata = imagedata
        self.name = json["name"]


class DBMap:
    def __init__(self, image_json, *tilesets):
        self._json = image_json
        self.tilesets = [*tilesets]
