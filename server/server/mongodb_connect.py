from pymongo import MongoClient

class Connect(object):
    connection = None
    url_pattern = "mongodb://{}:{}@{}/{}?authSource={}"

    @staticmethod
    def get_connection():
        if Connect.connection is None:
            username = "root"
            password = "password"
            hostlist = "185.199.99.158:8003"
            database = "units"
            authSource = "admin"
            url = Connect.url_pattern.format(username,password,hostlist,database,authSource)
            Connect.connection = MongoClient(url)
        return Connect.connection
