from .db_map import DBMap


class Config:
    def __init__(self):
        self.gl_map_height = 100
        self.gl_map_width = 100
        self.playable_teams = {1, 2}
        self.player_amount = 2

    def set_config(self, gl_map_width=100, gl_map_height=100, playable_teams={1, 2}):
        self.gl_map_height = gl_map_height
        self.gl_map_width = gl_map_width
        self.playable_teams = set(playable_teams)
        self.player_amount = len(self.playable_teams)

    def set_config_from_db_map(self, db_map : DBMap):
        self.gl_map_height = db_map.json["height"]
        self.gl_map_width = db_map.json["width"]

        #player amount is equal to number of teams
        #number of playable teams is equal to number
        #of castles with different teams execept neutral
        self.playable_teams = {DBMap.property(obj, "Team", 0)
                               for obj in db_map.objects()
                               if DBMap.is_castle(obj)} - {0}
        self.player_amount = len(self.playable_teams)
