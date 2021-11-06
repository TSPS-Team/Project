#!/usr/bin/env python3

from .server import *
import argparse
import json
from PIL import Image
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("map_json", type=Path, help="Path to map json")
    parser.add_argument("tileset_json", type=Path, help="Path to tileset json")
    parser.add_argument("image_path", type=Path, help="Path to image")
    args = parser.parse_args()

    server = None
    with args.map_json.open() as m:
        with args.tileset_json.open() as t:
            with args.image_path.open("rb") as i:
                m = DBMap(json.load(m),
                          Tileset(json.load(t),
                                  i.read()))
                server = Server(m)

    interface = server.get_interface()

    player_id = 1
    command = input()
    while command != "exit":
        direction = None
        if command == "w":
            direction = (0, 1)
        elif command == "a":
            direction = (-1, 0)
        elif command == "s":
            direction = (0, -1)
        elif command == "d":
            direction = (1, 0)

        interface.move(player_id, direction)
        print("Move")

        #image = interface.get_view(player_id)
        #image.save("out.png")
        command = input()
