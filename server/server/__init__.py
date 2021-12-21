#!/usr/bin/env python3

from .server import *
from PIL import Image
from pathlib import Path
from pymongo import MongoClient

class Connect(object):
    connection: MongoClient
    connection = None
    url_pattern = "mongodb://{}:{}@{}/{}?authSource={}"

    @staticmethod
    def get_connection() -> MongoClient:
        if Connect.connection is None:
            username = "root"
            password = "password"
            hostlist = "185.199.99.158:8003"
            database = "units"
            authSource = "admin"
            url = Connect.url_pattern.format(username,password,hostlist,database,authSource)
            Connect.connection = MongoClient(url)
        return Connect.connection

    @staticmethod
    def get_random_map() -> DBMap:
        db = Connect.connection["units"]

        maps_collection = db["maps"]

        jon = maps_collection.find_one()

        return DBMap(jon)

    @staticmethod
    def get_unit_data():
        db = Connect.connection["units"]

        units_collection = db["units"]
        return units_collection.find_one()

def main():
    Connect.get_connection()
    server = Server(Connect.get_random_map(), Connect.get_unit_data())

    interface = server.get_interface()

    player_id = 1
    command = input()
    while command != "exit":
        direction = None
        if command == "w":
            direction = (0, -1)
        elif command == "a":
            direction = (-1, 0)
        elif command == "s":
            direction = (0, 1)
        elif command == "d":
            direction = (1, 0)
        else:
            command = input()
            continue

        interface.move(player_id, direction)

        image = interface.get_view(player_id)
        image.save("out.png")
        command = input()
