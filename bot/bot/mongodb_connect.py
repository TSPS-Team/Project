from pymongo import MongoClient
from server.db_map import DBMap

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
    def get_map_by_player_count(player_count) -> DBMap:
        db = Connect.connection["units"]

        maps_collection = db["maps"]

        jon = maps_collection.find_one({
            "properties": {
                '$elemMatch': {"name": "Teams", "value": player_count}
            }})

        return DBMap(jon)

    @staticmethod
    def get_unit_data():
        db = Connect.connection["units"]

        units_collection = db["units"]
        return units_collection.find_one()
