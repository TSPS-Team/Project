import global_map
import game_config


class GameInstance:
    def __init__(self):
        game_config.set_config()
        _global_map = global_map.GlobalMap(game_config.Config.gl_map_width, game_config.Config.gl_map_height)

