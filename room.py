import copy

class Room:
    def __init__(self, configuration={}):
        self.doors = copy.deepcopy(configuration)

class Town(Room):
    def __init__(self, name, description, room_configuration={}, map_type='path'):
        super().__init__(room_configuration)
        self.name = name
        self.description = description
        self.map_type = map_type

class Wilderness(Room):
    def __init__(self, name, description, configuration, monster_percent, map_type='path'):
        super().__init__(configuration)
        self.name = name
        self.description = description
        self.monster_percent = monster_percent
        self.map_type = type

class Resource(Room):
    def __init__(self, name, description, configuration, item=None, weapon_required=None, map_type='path'):
        super().__init__(configuration)
        self.name = name
        self.description = description
        self.item = item
        self.weapon_required = weapon_required
        self.map_type = map_type