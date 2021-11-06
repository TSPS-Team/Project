#!/usr/bin/env python3
from PIL import Image
from ..db_map import Tileset

class TilesetRenderer:
    def __init__(self, tileset : Tileset):
        self.tileset = tileset

    def draw(self, layers, width, height) -> Image.Image:
        image = Image.new('RGBA',
                          (width * self.tileset.tilewidth,
                           height * self.tileset.tileheight))

        for layer in layers:
            for i, id in enumerate(layer):
                if (id == 0):
                    continue
                j = i % width
                k = i // width
                tile = self.tileset.get(id)

                image.paste(tile, (j * self.tileset.tilewidth, k * self.tileset.tileheight), tile)

        return image
