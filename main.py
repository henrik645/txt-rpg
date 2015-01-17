class Room:
    def __init__(self, configuration={}):
        self.doors = configuration

class Merchant:
    def __init__(self, markup=1.2, markdown=0.8):
        self.inventory = []
        self.markup = markup
        self.markdown = markdown
        
    def add_item(self, item):
        # Adds an item to the merchant's inventory
        
        if (not isinstance(item, Item)):
            raise TypeError("Unexpected " + type(item))

        self.inventory.append(item)

    def get_selling_offers(self):
        # Lists all items in the merchant's inventory
        # and adds the markup fee

        offers = []
        for item in self.inventory:
            offer = (item, item.value*self.markup)
            offers.append(offer)

        return offers

    def get_buying_offers(self, items):
        # Generates buying offers on the items in 'items'

        offers = []
        for item in items:
            offer = (item, item.value*self.markdown)
            offers.append(offer)

        return offers

class Town(Room):
    def __init__(self, name, description, room_configuration={}):
        super().__init__(room_configuration)
        self.name = name
        self.description = description

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
    def __init__(self, name, description, damage=0, value=0):
        self.damage = damage
        super().__init__(name, description, value)

class Player:
    def __init__(self, room, hp=100, inventory=[], armour=[]):
        self.room = room
        self.hp = hp
        self.inventory = inventory
        self.armour = armour
    
    def go_to(self, room):
        self.room = room
        
def view_selling_offers(merchant):
    selling_offers = merchant.merchant.get_selling_offers()

    selling_offers_formatted = []

    for offer in selling_offers:
        selling_offers_formatted.append((offer[0].name, offer[1]))

    for i in range(len(selling_offers_formatted)):
        print(str(i + 1) + " - " + selling_offers_formatted[i][0] + " - " + str(selling_offers_formatted[i][1]) + "G")

 
martins_way = []
town_square = Room()
martins_way.append(Room())
martins_way.append(Room())
tailor = Room()
blacksmith = Room()
        
town_square = Town("Town Square", "A stone brick fountain is located in the middle. You see farmers selling their goods.", {'north': martins_way[0]})
martins_way[0] = Town("Martin's Way", "A wide stone brick road", {'north':martins_way[1], 'south':town_square})
martins_way[1] = Town("Martin's Way", "A wide stone brick road", {'south':martins_way[0], 'west':tailor, 'east':blacksmith})
tailor = Town("Tailor", "A heavy-set man is standing behind the oak counter. You see sewing supplies in the back room.", {'east': martins_way[1]})
blacksmith = Town("Blacksmith", "A little stone building. You feel the heat from the forge.", {'west':martins_way[1]})

tailor.merchant = Merchant(1.0, 0.8)
blacksmith.merchant = Merchant(1.0, 0.8)

leather_jacket = Item("Leather Jacket", "A large leather jacket. The quality isn't that good.", 5)
leather_pants = Item("Leather Pants", "A pair of leather pants. The quality isn't that good.", 5)
iron_pickaxe = Weapon("Iron Pickaxe", "A simple iron pickaxe. Useful for mining", 10, 10)
iron_sword = Weapon("Iron Sword", "A simple iron sword. Useful for slaying enemies", 15, 20)
iron_axe = Weapon("Iron Axe", "A simple iron axe. Useful for cutting down trees", 10, 15)

tailor.merchant.add_item(leather_jacket)
tailor.merchant.add_item(leather_pants)
blacksmith.merchant.add_item(iron_pickaxe)
blacksmith.merchant.add_item(iron_sword)
blacksmith.merchant.add_item(iron_axe)

player = Player(town_square)

player.go_to(town_square) #Starting room is always town square.

while True:
    print(player.room.name)
    print(player.room)
    for i in range(30):
        print("")
    print(player.room.name)
    print(player.room.description)
    print(player.room.doors)
    print("Exits:")
    for exit in player.room.doors:
        print(exit.title() + " (" + player.room.name + ")")
    walk_to = input(">")
    print(player.room.doors[walk_to])
    player.go_to(player.room.doors[walk_to])