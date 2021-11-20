from .db_map import DBMap
from . import global_map
from . import game_config


class GameInstance:
    def __init__(self, db_map : DBMap):
        self._config = game_config.Config()
        self._config.set_config_from_db_map(db_map)
        self._global_map = global_map.GlobalMap(self._config, db_map)
