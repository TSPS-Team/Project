class ObjectWrapper:
    def __init__(self, castle=None, castle_coord=(), hero=None, hero_coord=()):
        self.castles = []
        if castle is not None:
            self.castles.append(castle)
            self.castles_coord = []
            self.castles_coord.append(castle_coord)

        self.heroes = []
        if hero is not None:
            self.heroes.append(hero)
            self.heroes_coord = []
            self.heroes_coord.append(hero_coord)

    def add_castle(self, castle, castle_coord):
        self.castles.append(castle)
        self.castles_coord.append(castle_coord)

    def add_hero(self, hero, hero_coord):
        self.heroes.append(hero)
        self.castles_coord.append(hero_coord)

    def del_castle(self):
        pass

    def del_hero(self):
        pass
