# immovable objects like road, wasteland, barracks


class MapObject:
    def __init__(self, object_id):
        self.object_id = object_id
        self.pathable = self.get_pathable(object_id)

    @staticmethod
    def get_pathable():
        pathable = True         # maybe we just have pathable objects have id lesser than X et cetera
        return pathable


class Terrain(MapObject):
    def __init__(self):
        pass


class Interactive(MapObject):
    def __init__(self):
        pass
