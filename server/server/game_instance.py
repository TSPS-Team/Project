from . import global_map
from . import game_config


class GameInstance:
    def __init__(self):
        _config = game_config.Config()
        _config.set_config()
        _global_map = global_map.GlobalMap(_config)

