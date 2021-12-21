#!/usr/bin/env python3
from PIL import Image
from ..db_map import Tileset
import bisect
import base64

class TilesetRenderer:
    first_gids: list[int]
    tilesets: list[Tileset]
    def __init__(self, tilesets_json: dict):
        self.tilesets_json = tilesets_json
        self.first_gids = []
        self.tilesets = []

        for tileset_json in self.tilesets_json:
            self.first_gids.append(tileset_json["firstgid"])
            self.tilesets.append(Tileset(tileset_json, base64.b64decode(tileset_json["image"])))

    def draw(self, layers, width, height) -> Image.Image:
        image = Image.new('RGBA',
                          (width * self.tilesets[0].tilewidth,
                           height * self.tilesets[0].tileheight))

        for layer in layers:
            for i, gid in enumerate(layer):
                if (gid == 0):
                    continue

                tileset_index = bisect.bisect_left(self.first_gids, gid) - 1
                tileset = self.tilesets[tileset_index]
                first_gid = self.first_gids[tileset_index]
                j = i % width
                k = i // width
                tile = tileset.get(gid - first_gid)

                image.paste(tile, (j * tileset.tilewidth, k * tileset.tileheight), tile)

        return image
