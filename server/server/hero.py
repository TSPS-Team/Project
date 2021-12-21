import numpy as np

class Hero:
    def __init__(self, hero_id=0, player_id=1, attack=0, deffence=0, intelligence=0, magic_resist=0, mana=0, speed=5):
        self.id = hero_id
        self.player_id = player_id
        self.hero_name = self.generate_name()

        self.attack = attack
        self.deffence = deffence
        self.intelligence = intelligence
        self.magic_resist = magic_resist
        self.mana = mana
        self.speed = speed + 1000
        self.stamina = speed + 1000

        self.army = np.full(7, None, dtype=np.object_)

        self.magic_book = None

    def get_stamina(self) -> int:
        return self.stamina

    def recover_stamina(self, recovery: int=None):
        if recovery is None:
            self.stamina = self.speed
        else:
            self.stamina += recovery

    def moving(self) -> int:
        if self.able_to_move():
            self.stamina -= 1
            return 0
        return -1

    def able_to_move(self) -> bool:
        return True if self.stamina>0 else False

    @staticmethod
    def generate_name() -> str:
        return "Napoleon"


