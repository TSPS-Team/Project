#!/usr/bin/env python3

import pytest
from server.hero import Hero

def test_can_move():
    hero = Hero()

    hero.stamina = 0;
    assert(hero.able_to_move() is False)

def test_moving():
    hero = Hero()

    hero.stamina = 5;
    assert(hero.able_to_move() is True)
    hero.moving()
    hero.moving()
    hero.moving()
    hero.moving()
    assert(hero.able_to_move() is True)
    hero.moving()
    assert(hero.able_to_move() is False)


def test_recover_stamina():
    hero = Hero(speed=1)
    hero.moving()
    assert(hero.able_to_move() is False)
    hero.recover_stamina()
    assert(hero.able_to_move() is True)
