from enum import Enum

from .states import GlobalState, ServerState
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
        #TODO

        can_move, player = self.check_can_move_simultaniously()
        if can_move:
            return ServerState(GlobalState.WaitingForActionEvery)
        else:
            #TODO
            return ServerState(GlobalState.WaitingForActionOne, player=player)

    def check_can_move_simultaniously(self):
        #TODO
        return [True, None]

    def start_of_week(self):
        #TODO
        pass
