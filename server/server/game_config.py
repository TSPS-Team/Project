class Config:
    def __init__(self):
        self.gl_map_height = 100
        self.gl_map_width = 100
        self.player_amount = 2

    def set_config(self, gl_map_width=100, gl_map_height=100, player_amount=2):
        self.gl_map_height = gl_map_height
        self.gl_map_width = gl_map_width
        self.player_amount = player_amount
