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
    def __init__(self, name, room_configuration={}):
        super().__init__(room_configuration)
        self.name = name

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



# Create new place with the name "My Place"
my_place = Town("My Place")

# Create new merchant with markup=1.2 and markdown=0.8
my_merchant = Merchant(1.2, 0.8)

# Attach the merchant to the place
my_place.merchant = my_merchant

# Create new weapon with the name "Sword", the description "A plain sword."
# a damage value of 20, and a monetary value of 10
sword = Weapon("Sword", "A plain sword.", 20, 10)

# Ditto
axe = Weapon("Axe", "A plain axe.", 30, 20)

# Ditto
pickaxe = Weapon("Pickaxe", "A plain pickaxe.", 10, 10)

# Add our weapons to the merchant we attached to our place
my_place.merchant.add_item(sword)
my_place.merchant.add_item(axe)
my_place.merchant.add_item(pickaxe)

# Create a new room
# Pass the configuration dict, which says that the east door should lead to my_place
starting_room = Room({'east': my_place})

# Get selling offers from the merchant in the place that is behind the east door of our room
selling_offers = starting_room.doors['east'].merchant.get_selling_offers()

selling_offers_formatted = []

for offer in selling_offers:
    selling_offers_formatted.append((offer[0].name, offer[1]))
    
print(selling_offers_formatted)