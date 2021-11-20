import numpy as np


class Castle:
    def __init__(self):
        self.town_hall_lvl = 1
        self.magic_tower_lvl = 0
        self.units_lvl = np.zeros(7, dtype=np.uint8)
        self.units_increase = np.zeros(7, dtype=np.uint8)
        self.units_amount = np.zeros(7, dtype=np.uint64)
        self.units_price = np.array([20, 50, 80, 180, 500, 1100, 4000], dtype=np.uint64)

    def get_income(self) -> int:
        return self.town_hall_lvl*2000-1000