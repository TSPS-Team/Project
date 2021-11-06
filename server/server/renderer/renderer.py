#!/usr/bin/env python3
from PIL import Image
from ..db_map import Tileset

class TilesetRenderer:
    def __init__(self, tileset : Tileset):
        self.tileset = tileset
        self.tileset_image = Image.open(tileset.imagedata)

    def id_to_image(self, id) -> Image.Image:
        assert(id < self.tileset.tilecount)

        i = id % self.tileset.columns
        j = id // self.tileset.columns
        width = self.tileset.tilewidth
        height = self.tileset.tileheight

        rect = (i * width, j * height,
                (i + 1) * width, (j + 1) * height)
        return self.tileset_image.crop(rect)

    def draw(self, layers, width, height) -> Image.Image:
        image = Image.new('RGBA',
                          (width * self.tileset.tilewidth,
                           height * self.tileset.tileheight))

        for layer in layers:
            for i, id in enumerate(layer):
                j = i % width
                k = i // height
                tile = self.id_to_image(id)

                image.paste(tile, j * width, k * height)

        return image
