#!/usr/bin/env python3
from .mongodb_connect import Connect

class AppInfo:
    def __init__(self):
        self.lobby_manager = None
        self.mongodb_connection = Connect.get_connection()
