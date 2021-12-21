#!/usr/bin/env python3
from PIL import Image
import PIL
from ..db_map import Tileset
import bisect
import base64

class TilesetRenderer:
    first_gids: list[int]
    tilesets: list[Tileset]
    template: Image.Image
    fog: Image.Image
    width: int
    height: int
    def __init__(self, tilesets_json: dict, width, height):
        self.tilesets_json = tilesets_json
        self.first_gids = []
        self.tilesets = []
        self.template = None
        self.width = width
        self.height = height

        for tileset_json in self.tilesets_json:
            self.first_gids.append(tileset_json["firstgid"])
            self.tilesets.append(Tileset(tileset_json, base64.b64decode(tileset_json["image"])))

        self.fog = Image.new(mode = "RGBA", size =
                             (self.tilesets[0].tilewidth, self.tilesets[1].tileheight),
                             color = (0, 0, 0, 255))

    def put(self, image, x, y, gid, color=(0,0,0,0)):
        if (gid == 0):
            return

        tileset_index = bisect.bisect_left(self.first_gids, gid) - 1
        tileset = self.tilesets[tileset_index]
        first_gid = self.first_gids[tileset_index]
        tile = tileset.get(gid - first_gid)

        if color[3] != 0:
            mask = Image.new(mode = "RGBA", size =
                             (self.tilesets[0].tilewidth, self.tilesets[1].tileheight),
                             color=color)

            tmp = Image.new(mode = "RGBA", size =
                            (self.tilesets[0].tilewidth, self.tilesets[1].tileheight),
                            color=(0,0,0,0))

            tmp.paste(mask, None, tile)
            mask.putalpha(255)

            tile.paste(mask, None, tmp)

        image.paste(tile, (x * tileset.tilewidth, y * tileset.tileheight), tile)


    def apply_image(self, image, x, y, tile):
        image.paste(tile, (x * self.tilesets[0].tilewidth,
                           y * self.tilesets[1].tileheight), tile)

    def draw(self, layers) -> Image.Image:
        image = Image.new('RGBA',
                          (self.width * self.tilesets[0].tilewidth,
                           self.height * self.tilesets[0].tileheight))

        for layer in layers:
            for i, gid in enumerate(layer):
                if (gid == 0):
                    continue

                tileset_index = bisect.bisect_left(self.first_gids, gid) - 1
                tileset = self.tilesets[tileset_index]
                first_gid = self.first_gids[tileset_index]
                j = i % self.width
                k = i // self.width
                tile = tileset.get(gid - first_gid)

                image.paste(tile, (j * tileset.tilewidth, k * tileset.tileheight), tile)

        return image
