from enum import Enum
from .db_map import DBMap
from . import global_map
from . import game_config

class DayOfWeek(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

    def next(self):
        return DayOfWeek((self.value + 1) % 7)


class GameInstance:
    def __init__(self, db_map : DBMap):
        self._config = game_config.Config()
        self._config.set_config_from_db_map(db_map)
        self._global_map = global_map.GlobalMap(self._config, db_map)

        self.day_of_week = DayOfWeek.Monday

    def next_day(self):
        self.day_of_week = self.day_of_week.next()

        if self.day_of_week == DayOfWeek.Monday:
            self.start_of_week()

    def start_of_week(self):
        self._global_map.start_of_week()

    def move_hero(self, object_id, direction: str) -> int:
        return self._global_map.move_hero(object_id, direction)                 # -1 cannot move / 0 all good

    def run(self):
        while True:
            pass
