#!/usr/bin/env python3

import pytest
from server.global_map import GlobalMap
from server.game_config import Config
from server.unit_dictionary import UnitDictionary


def test_no_throw():
    map = GlobalMap(Config(), None, UnitDictionary())

def test_move():
    map = GlobalMap(Config(), None, UnitDictionary())
    object_id = (2, "hero", 0)

    map.move_hero(object_id, "ru")
