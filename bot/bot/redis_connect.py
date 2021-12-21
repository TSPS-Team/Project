#!/usr/bin/env python3


import redislite
import redis

def get_reddis_connection() -> redis.Redis:
    connection = redis.Redis(
        host="localhost",
        port=6379,
        db=2
    )

    try:
        connection.ping()
    except redis.exceptions.ConnectionError:
        connection = redislite.Redis()
        connection.ping()

    return connection
