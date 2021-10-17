# immovable objects like road, wasteland, barracks


class MapChank:
    def __init__(self, chank_id=0):
        self.object_id = chank_id
        self.pathable = self.get_pathable(chank_id)

    @staticmethod
    def get_pathable():
        pathable = True         # maybe we just make pathable objects have id lesser than X et cetera
        return pathable


class Terrain(MapChank):
    def __init__(self):
        pass


class Interactive(MapChank):
    def __init__(self):
        pass
