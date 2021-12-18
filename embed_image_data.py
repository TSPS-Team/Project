#!/usr/bin/env python3

from pathlib import Path
import argparse
import json
import base64

import sys
import contextlib

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path, help="Path to map json to embed images into")
    parser.add_argument("--output", "-o", type=Path, default="-", help="Path to output json")

    args = parser.parse_args()


    data = json.load(args.file.open())

    for tileset in data["tilesets"]:
        image_path = args.file.parent / Path(tileset["image"])
        tileset["image"] = base64.b64encode(image_path.open("rb").read()).decode()


    with smart_open(str(args.output)) as f:
        json.dump(data, f, indent=4)
