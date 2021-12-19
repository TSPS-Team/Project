#!/usr/bin/env python3

import pytest
from server.castle import Castle
from server.unit_dictionary import UnitDictionary

def test_income_increase():
    dic = UnitDictionary()
    castle = Castle(dic)

    old_income = castle.get_income()
    castle.lvlup_town_hall()
    new_income = castle.get_income()

    assert(old_income < new_income)
