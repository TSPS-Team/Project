class Hero:
    def __init__(self, hero_id=0, player_id=1, attack=0, deffence=0, intelligence=0, magic_resist=0, mana=0, speed=5):
        self.id = hero_id
        self.player_id = player_id
        self.hero_name = self.get_name()

        self.attack = attack
        self.deffence = deffence
        self.intelligence = intelligence
        self.magic_resist = magic_resist
        self.mana = mana
        self.speed = speed

#        self.army =


    @staticmethod
    def get_name() -> str:
        pass
