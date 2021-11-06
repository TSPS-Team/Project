# immovable objects like road, wasteland, barracks


class MapChankFirstLayer:
    def __init__(self, chank_id=0, pathable=True):
        self.object_id = chank_id
        self.pathable = pathable

    def get_pathable(self):
        return self.pathable


class Terrain(MapChankFirstLayer):
    def __init__(self):
        pass


class Road(Terrain):
    def __init__(self):
        pass


class Interactive(MapChankFirstLayer):
    def __init__(self):
        pass
