#!/usr/bin/env python3

class Tileset:
    def __init__(self, json, imagedata):
        self._json = json
        self.imagedata = imagedata
        self.tilewidth = json["tilewidth"]
        self.tilecount = json["tilecount"]
        self.tileheight = json["tileheight"]
        self.columns = json["columns"]
        self.name = json["name"]


class DBMap:
    def __init__(self, image_json, entities_tileset, *tilesets):
        self._json = image_json
        self.entities_tileset = entities_tileset
        self.tilesets = [*tilesets]
