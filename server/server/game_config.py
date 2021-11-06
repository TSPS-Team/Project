class Config:
    def __init__(self):
        self.gl_map_height = 100
        self.gl_map_width = 100

    def set_config(self, gl_map_width=100, gl_map_height=100):
        self.gl_map_height = gl_map_height
        self.gl_map_width = gl_map_width
