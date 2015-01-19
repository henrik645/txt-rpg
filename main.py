import sys
import copy
import random

class Room:
    def __init__(self, configuration={}):
        self.doors = copy.deepcopy(configuration)

class Wilderness(Room):
    def __init__(self, name, description, configuration, monster_percent):
        super().__init__(configuration)
        self.name = name
        self.description = description
        self.monster_percent = monster_percent

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

#Types of items are: Item (Normal item), Consumable (Removed after use) and Armour (Normal armour. Defense level is stored at defense) If any item restores HP, the
#maximum amount of HP restored is stored at hp_restore

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

class Consumable(Item):
    def __init__(self, name, description, value, hp_restore=0):
        self.hp_restore = hp_restore
        super().__init__(name, description, value)

class Armour(Item):
    def __init__(self, name, description, value, defense=0, level_required=1):
        self.defense = defense
        self.level_required = level_required
        super().__init__(name, description, value)

class Player:
    def __init__(self, room, hp=100, max_hp=100, defense=0, money=100, inventory=[], armour=[], killed=False, in_fight=False):
        self.room = room
        self.hp = hp
        self.max_hp = max_hp
        self.inventory = inventory
        self.armour = armour
        self.defense = defense
        self.money = money
        self.killed = killed
        self.in_fight = in_fight
    
    def go_to_room(self, room):
        self.room = room
    
    def view_inventory(self, use_menu=False):
        if len(self.inventory) > 0:
            items_formatted = []
            
            for item in self.inventory:
                items_formatted.append(item.name)
            
            print("  - Inventory -  ")
            
            count = 0
            if use_menu:
                for item in items_formatted:
                    print(" " + str(count) + " " + item)
                    count += 1
            else:
                for item in items_formatted:
                    print(" * " + item)
    
    def view_equipment(self):
        if len(self.armour) > 0:
            items_formatted = []
            
            for item in self.armour:
                items_formatted.append(item.name)
            
            print("  - Equipment -  ")
            
            for item in items_formatted:
                print(" * " + item)
      
class Monster:
    def __init__(self, name, max_hp, hp_per_hit):
        self.name = name
        self.hp = max_hp
        self.max_hp = max_hp
        self.hp_per_hit = hp_per_hit
    
def view_selling_offers(merchant):
    selling_offers = merchant.merchant.get_selling_offers()

    selling_offers_formatted = []

    for offer in selling_offers:
        selling_offers_formatted.append((offer[0].name, offer[1]))

    for i in range(len(selling_offers_formatted)):
        print(str(i + 1) + " - " + selling_offers_formatted[i][0] + " - " + str(selling_offers_formatted[i][1]) + "G")

monster_percent_north_gate = [{'name': 'Wolf', 'level': 1, 'percent': 0.3}, {'name': 'Zombie' ,'level': 2, 'percent': 0.5}]

class Loot_table():
    def __init__(self, list):
        self.list = list
    def choose_from_list(self):
        random.seed()
        percent_absolute = []
        percent_cumulative = []
        cumulative = 0
        chosen = None
        for percent in self.list:
            percent_absolute.append(percent['percent'])
            percent_cumulative.append(percent['percent'] + cumulative)
            cumulative += percent['percent']
            
        default = 1 - cumulative
        
        random_num = random.random()
        for i, percent in enumerate(percent_cumulative):
            if percent > random_num:
                chosen = self.list[i]
                break
        
        return(chosen)
    
directions = {'n': 'north', 'e': 'east', 's': 'south', 'w': 'west'}

town_square = Town("Town Square", "A stone brick fountain is located in the middle. You see farmers selling their goods.")
tailor = Town("Tailor", "You see sewing supplies in the back.")
martins_way = [Town("Martin's Way 1", "A wide stone brick road."), Town("Martin's Way 2", "A wide stone brick road.")]
blacksmith = Town("Blacksmith", "A little stone building. You feel the heat from the forge as soon as you step in.")
north_gate = Wilderness("North Gate", "A high valved gate. Two guards are patrolling everyone coming in.", {}, Loot_table([{'name': 'Wolf', 'level':1, 'percent': 0.75}]))

monsters = [{'name': 'Wolf', 'max_hp': 25, 'hp_per_hit': 5}]

tailor.doors['east'] = martins_way[1]
town_square.doors['north'] = martins_way[0]
town_square.doors = {'north': martins_way[0]}
martins_way[0].doors['north'] = martins_way[1]
martins_way[0].doors['south'] = town_square
martins_way[1].doors['east'] = blacksmith
martins_way[1].doors['south'] = martins_way[0]
martins_way[1].doors['west'] = tailor
martins_way[1].doors['north'] = north_gate
north_gate.doors['south'] = martins_way[1]
blacksmith.doors['west'] = martins_way[1]

tailor.merchant = Merchant(1.0, 0.8)
blacksmith.merchant = Merchant(1.0, 0.8)

leather_jacket = Armour("Leather Jacket", "A large leather jacket. The quality isn't that good.", 5, 10)
leather_pants = Armour("Leather Pants", "A pair of leather pants. The quality isn't that good.", 5, 10)
iron_pickaxe = Weapon("Iron Pickaxe", "A simple iron pickaxe. Useful for mining", 10, 10)
iron_sword = Weapon("Iron Sword", "A simple iron sword. Useful for slaying enemies", 15, 20)
iron_axe = Weapon("Iron Axe", "A simple iron axe. Useful for cutting down trees", 10, 15)
apple = Consumable("Apple", "A tasty apple", 3, 10)

tailor.merchant.add_item(leather_jacket)
tailor.merchant.add_item(leather_pants)
blacksmith.merchant.add_item(iron_pickaxe)
blacksmith.merchant.add_item(iron_sword)
blacksmith.merchant.add_item(iron_axe)
tailor.merchant.add_item(apple)

player = Player(town_square) #Starting room is always town square.

refresh = True
player.inventory.append(iron_sword)
player.inventory.append(iron_axe)

while True:
    if player.killed:
        player.killed = False
        player.go_to_room(town_square) #Town square is respawn point
        player.hp = player.max_hp
        print("You respawned at " + player.room.name + ".")
        print("")
        refresh = True
    if refresh:
        for i in range(30):
            print("")
        refresh = False
        print(player.room.name)
        print(player.room.description)
        if isinstance(player.room, Wilderness):
            chosen_monster = player.room.monster_percent.choose_from_list()
            if chosen_monster is not None:
                print("You have been attacked by a level " + str(chosen_monster['level']) + " " + str(chosen_monster['name']) + "!")
                player.in_fight = True
                for i, monster in enumerate(monsters):
                    if monster['name'] == chosen_monster['name']:
                        fight_monster = Monster(chosen_monster['name'], monsters[i]['max_hp'], monsters[i]['hp_per_hit'])
        if hasattr(player.room, 'merchant') and not player.in_fight:
            print("")
            print("A merchant is present.")
            view_selling_offers(player.room)
            print("Enter number to buy.")
        if not player.in_fight:
            print("")
            print("Exits:")
            for exit in player.room.doors:
                print(exit.title() + " (" + player.room.doors[exit].name + ")")
    walk_to = input(">")
    walk_to = walk_to.lower()
    if walk_to == 'g' or walk_to == 'gold':
        print("Gold: " + str(player.money))
        print("HP: " + str(player.hp))
        print("Defense: " + str(player.defense))
    elif walk_to == 'i' or walk_to == 'inventory':
        player.view_inventory()
        print("")
        player.view_equipment()
    elif walk_to == 'u' or walk_to == 'use':
        player.view_inventory(True)
        player.view_equipment()
        print("Enter number to use or equip.")
        use = input(">")
        if use.isdigit():
            use = int(use)
            if use >= 0 and use <= len(player.inventory) and len(player.inventory) > 0:
                if isinstance(player.inventory[use], Consumable):
                    if player.hp + player.inventory[use].hp_restore > player.max_hp:
                        player.hp = player.max_hp
                        print("You were restored to " + str(player.max_hp) + " HP.")
                    else:
                        player.hp += player.inventory[use].hp_restore
                        print("You were restored to " + str(player.hp + player.inventory[use].hp_restore) + " HP.")
                    player.inventory.pop(use)
                elif isinstance(player.inventory[use], Armour):
                    player.armour.append(player.inventory[use]) #Appends value to equipment.
                    item = player.inventory.pop(use) #Removes value from inventory.
                    player.defense += item.defense
                    print("Equipped item.")
                    print("Your Defense level is " + str(player.defense))
                elif isinstance(player.inventory[use], Weapon) and player.in_fight:
                    print("You hit the " + fight_monster.name + " with your " + player.inventory[use].name + "!")
                    fight_monster.hp -= player.inventory[use].damage
                    if fight_monster.hp <= 0:
                        print("The " + fight_monster.name + " died!")
                        player.in_fight = False
                    else:                        
                        print(fight_monster.name + " HP: " + str(fight_monster.hp) + " / " + str(fight_monster.max_hp))
                        print("The " + fight_monster.name + " hit you!")
                        player.hp -= fight_monster.hp_per_hit
                        if player.hp <= 0:
                            print("The " + fight_monster.name + " killed you!")
                            player.in_fight = False
                            player.killed = True
                        else:
                            print("Your HP: " + str(player.hp) + " / " + str(player.max_hp))
                else:
                    print("This item can not be equipped.")
               
    else:
        for dir_abbr, direction in directions.items():
            if direction in player.room.doors:
                if walk_to == dir_abbr and player.in_fight == False:
                    player.go_to_room(player.room.doors[direction])
                    refresh = True
                    break
                elif walk_to.lower() == direction:
                    player.go_to_room(player.room.doors[direction])
                    refresh = True
                    break
                elif player.in_fight:
                    print("You can not leave while in a fight!")
        try:  #Tries if walk_to (player input) is a number, meaning that the player have chosen to buy an item.
            walk_to = int(walk_to)
            selling_offers = player.room.merchant.get_selling_offers()
            walk_to -= 1
            if walk_to >= 0 and walk_to <= len(selling_offers):
                if player.money < selling_offers[walk_to][1]:
                    print("You are not in possession of enough gold.")
                else:
                    print("You have bought: " + selling_offers[walk_to][0].name)
                    player.money -= selling_offers[walk_to][1]
                    player.inventory.append(selling_offers[walk_to][0])
            else:
                print("You cannot find this item in this store.")
        except:
            pass