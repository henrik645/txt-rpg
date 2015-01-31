class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value # The item's monetary value

        @property
        def value(self):
            return self.value

        @value.setter
        def x(self, value):
            if value < 0:
                raise ValueError("Item value cannot be less than 0")
            else:
                self.value = value

class Weapon(Item):
    def __init__(self, name, description, slot, damage=0, value=0, level_required=1):
        self.damage = damage
        self.slot = slot
        self.level_required = level_required
        super().__init__(name, description, value)

class Consumable(Item):
    def __init__(self, name, description, value, hp_restore=0):
        self.hp_restore = hp_restore
        super().__init__(name, description, value)

class Armour(Item):
    def __init__(self, name, description, slot, value, defense=0, level_required=1):
        self.defense = defense
        self.level_required = level_required
        self.slot = slot
        super().__init__(name, description, value)