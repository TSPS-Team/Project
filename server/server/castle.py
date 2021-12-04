import numpy as np
from . import magic_book

class Castle:
    def __init__(self, unit_dict ,type="rampart"):
        self.town_hall_lvl = 1
        self.magic_tower_lvl = 0
        self.magic_book = magic_book.MagicBook()
        self.units_lvl = np.zeros(7, dtype=np.uint8)
        self.units_increase = np.zeros(7, dtype=np.uint8)                                       # how many units come every week
        self.units_amount_available = np.zeros(7, dtype=np.uint64)                              # how many u can buy at moment
        temp = list()
        for i in range(1,8):
            temp.append(unit_dict.stat_dictionary.get(type+str(i)).get("price"))
        self.units_price = np.array(temp, dtype=np.uint64)

        self.garrison = np.full(7, None, dtype=np.object_)                                      # garrison, can be exchanged with hero
        self.staying_hero = None

        self.type = type

    def get_income(self) -> int:
        return self.town_hall_lvl*2000-1000

    def lvlup_town_hall(self) -> int:
        if self.town_hall_lvl == 3:
            return -1
        else:
            self.town_hall_lvl += 1
            return 0

    def lvlup_magic_tower(self) -> int:
        if self.magic_tower_lvl == 5:
            return -1
        else:
            self.magic_tower_lvl += 1
            return 0

    def lvlup_unit(self, unit_lvl: int) -> int:             # upgrade units in "shop"
        if self.units_lvl[unit_lvl] == 2:
            return -1
        else:
            if self.units_lvl[unit_lvl] == 0:
                self.units_increase[unit_lvl] = self.calc_increase(unit_lvl)
                self.units_amount_available[unit_lvl] = self.units_increase[unit_lvl] // 2
            self.units_lvl[unit_lvl] += 1
            return 0

    def conscription(self):
        for i in range(7):
            self.units_amount_available[i] += self.units_increase[i]

    def end_of_week(self):
        self.conscription()

    @staticmethod
    def calc_increase(unit_lvl) -> int:
        return abs(unit_lvl-7)*2-1+(unit_lvl-5)*(unit_lvl-5)