class UnitDictionary:       #name, attack, deffence, speed, damage, max_health, flying, range_attack, price
    def __init__(self):
        self.stat_dictionary = {
            "rampart1": {"name":"centaur",
                         "attack": 5,
                         "deffence": 3,
                         "speed": 6,
                         "damage": 2,
                         "max_health": 8,
                         "flying": False,
                         "range_attack": False,
                         "price": 70,},
            "rampart2": {"name": "dwarf",
                         "attack": 6,
                         "deffence": 3,
                         "speed": 3,
                         "damage": 3,
                         "max_health": 20,
                         "flying": False,
                         "range_attack": False,
                         "price": 120},
            "rampart3": {"name": "wood elf",
                         "attack": 9,
                         "deffence": 5,
                         "speed": 6,
                         "damage": 4,
                         "max_health": 15,
                         "flying": False,
                         "range_attack": True,
                         "price": 200},
            "rampart4": {"name": "pegasus",
                         "attack": 9,
                         "deffence": 8,
                         "speed": 8,
                         "damage": 7,
                         "max_health": 30,
                         "flying": True,
                         "range_attack": False,
                         "price": 250},
            "rampart5": {"name": "dendroid",
                         "attack": 9,
                         "deffence": 12,
                         "speed": 3,
                         "damage": 12,
                         "max_health": 55,
                         "flying": False,
                         "range_attack": False,
                         "price": 350},
            "rampart6": {"name": "unicorn",
                         "attack": 15,
                         "deffence": 14,
                         "speed": 7,
                         "damage": 20,
                         "max_health": 90,
                         "flying": False,
                         "range_attack": False,
                         "price": 850},
            "rampart7": {"name": "green dragon",
                         "attack": 18,
                         "deffence": 18,
                         "speed": 10,
                         "damage": 45,
                         "max_health": 180,
                         "flying": True,
                         "range_attack": False,
                         "price": 2400},

            "castle1": {"name": "pikeman",
                        "attack": 4,
                        "deffence": 5,
                        "speed": 4,
                        "damage": 2,
                        "max_health": 10,
                        "flying": False,
                        "range_attack": False,
                        "price": 60},
            "castle2": {"name": "archer",
                        "attack": 6,
                        "deffence": 3,
                        "speed": 4,
                        "damage": 2,
                        "max_health": 10,
                        "flying": False,
                        "range_attack": True,
                        "price": 100},
            "castle3": {"name": "griffin",
                        "attack": 8,
                        "deffence": 8,
                        "speed": 6,
                        "damage": 4,
                        "max_health": 25,
                        "flying": True,
                        "range_attack": False,
                        "price": 200},
            "castle4": {"name": "swordsman",
                        "attack": 10,
                        "deffence": 12,
                        "speed": 5,
                        "damage": 7,
                        "max_health": 35,
                        "flying": False,
                        "range_attack": False,
                        "price": 300},
            "castle5": {"name": "monk",
                        "attack": 12,
                        "deffence": 7,
                        "speed": 5,
                        "damage": 11,
                        "max_health": 30,
                        "flying": False,
                        "range_attack": True,
                        "price": 400},
            "castle6": {"name": "cavalier",
                        "attack": 15,
                        "deffence": 15,
                        "speed": 7,
                        "damage": 20,
                        "max_health": 100,
                        "flying": False,
                        "range_attack": False,
                        "price": 100},
            "castle7": {"name": "angel",
                        "attack": 20,
                        "deffence": 20,
                        "speed": 12,
                        "damage": 50,
                        "max_health": 200,
                        "flying": True,
                        "range_attack": False,
                        "price": 3000},

            "inferno1": {"name": "imp",
                         "attack": 2,
                         "deffence": 3,
                         "speed": 5,
                         "damage": 1,
                         "max_health": 4,
                         "flying": False,
                         "range_attack": False,
                         "price": 50},
            "inferno2": {"name": "gog",
                         "attack": 6,
                         "deffence": 4,
                         "speed": 4,
                         "damage": 3,
                         "max_health": 13,
                         "flying": False,
                         "range_attack": True,
                         "price": 125},
            "inferno3": {"name": "hell hound",
                         "attack": 10,
                         "deffence": 6,
                         "speed": 7,
                         "damage": 4,
                         "max_health": 25,
                         "flying": False,
                         "range_attack": False,
                         "price": 200},
            "inferno4": {"name": "demon",
                         "attack": 10,
                         "deffence": 10,
                         "speed": 5,
                         "damage": 8,
                         "max_health": 35,
                         "flying": False,
                         "range_attack": False,
                         "price": 250},
            "inferno5": {"name": "pit fiend",
                         "attack": 13,
                         "deffence": 13,
                         "speed": 6,
                         "damage": 15,
                         "max_health": 45,
                         "flying": False,
                         "range_attack": False,
                         "price": 500},
            "inferno6": {"name": "efreeti",
                         "attack": 16,
                         "deffence": 12,
                         "speed": 9,
                         "damage": 20,
                         "max_health": 90,
                         "flying": True,
                         "range_attack": False,
                         "price": 900},
            "inferno7": {"name": "devil",
                         "attack": 19,
                         "deffence": 21,
                         "speed": 11,
                         "damage": 35,
                         "max_health": 160,
                         "flying": True,
                         "range_attack": False,
                         "price": 2700},

            "dungeon1": {"name": "ded tarASS",
                         "attack": 2,
                         "deffence": 3,
                         "speed": 5,
                         "damage": 2,
                         "max_health": 8,
                         "flying": False,
                         "range_attack": False,
                         "price": 50},
            "dungeon2": {"name": "Maga",
                         "attack": 7,
                         "deffence": 3,
                         "speed": 3,
                         "damage": 3,
                         "max_health": 10,
                         "flying": True,
                         "range_attack": False,
                         "price": 110},
            "dungeon3": {"name": "Nujniy",
                         "attack": 9,
                         "deffence": 7,
                         "speed": 5,
                         "damage": 5,
                         "max_health": 22,
                         "flying": False,
                         "range_attack": True,
                         "price": 250},
            "dungeon4": {"name": "evGenius",
                         "attack": 10,
                         "deffence": 10,
                         "speed": 5,
                         "damage": 8,
                         "max_health": 25,
                         "flying": False,
                         "range_attack": True,
                         "price": 300},
            "dungeon5": {"name": "Lesha Random",
                         "attack": 15,
                         "deffence": 13,
                         "speed": 6,
                         "damage": 18,
                         "max_health": 50,
                         "flying": False,
                         "range_attack": False,
                         "price": 500},
            "dungeon6": {"name": "Maxus",
                         "attack": 17,
                         "deffence": 13,
                         "speed": 8,
                         "damage": 18,
                         "max_health": 80,
                         "flying": True,
                         "range_attack": False,
                         "price": 850},
            "dungeon7": {"name": "DeNiCoN",
                         "attack": 20,
                         "deffence": 20,
                         "speed": 11,
                         "damage": 45,
                         "max_health": 180,
                         "flying": True,
                         "range_attack": False,
                         "price": 2500},
        }