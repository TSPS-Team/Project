class ObjectWrapper:
    def __init__(self, castle=None, hero=None):
        self.castles = []
        self.castles.append(castle)

        self.heroes = []
        self.heroes.append(hero)

    def add_castle(self, castle):
        self.castles.append(castle)

    def add_hero(self, hero):
        self.heroes.append(hero)

    def del_castle(self):
        pass

    def del_hero(self):
        pass
