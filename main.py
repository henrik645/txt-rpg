import sys
import copy
import random
import math
import json
import os.path

class Room:
    def __init__(self, configuration={}):
        self.doors = copy.deepcopy(configuration)

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
    def __init__(self, name, description, room_configuration={}, map_type='path'):
        super().__init__(room_configuration)
        self.name = name
        self.description = description
        self.map_type = map_type

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
    def __init__(self, room, hp=100, max_hp=100, defense=0, money=100, inventory=[], armour=[], killed=False, in_fight=False, level=1):
        self.room = room
        self.hp = hp
        self.max_hp = max_hp
        self.inventory = inventory
        self.armour = armour
        self.defense = defense
        self.money = money
        self.killed = killed
        self.in_fight = in_fight
        self.level = level
    
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
    
        if len(self.armour) > 0:
            items_formatted = []
            
            for item in self.armour:
                items_formatted.append(item.name)
            
            print("")
            print("  - Equipment -  ")
            
            if use_menu:
                for i, item in enumerate(items_formatted):
                    print(" " + str(i + len(self.inventory)) + " " + item)
            else:
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

def convert_rooms(list):
    object_list = []
    for i, row in enumerate(list):
        object_row = []
        for n, room in enumerate(row):
            if room['name'] != False:
                if room['type'] == "Town":
                    object_row.append(Town(room['name'], room['description'], {}, room['map']))
                elif room['type'] == "Wilderness" and len(room['type']) >= 1:
                    object_row.append(Wilderness(room['name'], room['description'], {}, room['args'][1], room['map'])) #room['args'] represents arguments.
                elif room['type'] == "Resource" and len(room['type']) >= 2:
                    object_row.append(Resource(room['name'], room['description'], {}, room['args'][1], room['args'][2], room['map'])) #room['args'] represents arguments.
                else:
                    object_row.append(False)
                if room['args'] != []:
                    object_row[n].merchant = Merchant(1.0, 0.8)
                    for item in room['args']:
                        object_row[n].merchant.add_item(items[item])
                
            else:
                object_row.append(False)
        object_list.insert(0, object_row)
    
    for n, row in enumerate(object_list):
        for i, item in enumerate(row):
            if item != False:
                if i < len(object_list[n]) - 1:
                    if object_list[n][i + 1] is not False:
                        item.doors['east'] = object_list[n][i + 1]
                if i > 0:
                    if object_list[n][i - 1] is not False:
                        item.doors['west'] = object_list[n][i - 1]
                if n < len(object_list) - 1:
                    if object_list[n + 1][i] is not False:
                        item.doors['north'] = object_list[n + 1][i]
                if n > 0:
                    if object_list[n - 1][i] is not False:
                        item.doors['south'] = object_list[n - 1][i]
                    
    return(object_list)

# name, description, value, arguments
#
# item[0] = name
# item[1] = description
# item[2] = value
# item[3] = type
# item[4][0] = arg1
# item[4][1] = arg2
#
# Types: 'Weapon', 'Armour', 'Item', 'Consumable'
#
# Arguments:
# Weapon: Damage
# Consumable: HP restored
# Armour: Defense, Level required
    
def convert_items(list):
    object_list = []
    for item in list:
        if item['type'] == 'Weapon' and item['args'][0] is not None:
            object_list.append(Weapon(item['name'], item['description'], item['args'][0], item['value']))
        elif item['type'] == 'Armour' and item['args'][0] is not None and item['args'][1] is not None:
            object_list.append(Armour(item['name'], item['description'], item['value'], item['args'][0], item['args'][1]))
        elif item['type'] == 'Item':
            object_list.append(Item(item['name'], item['description'], item['value']))
        elif item['type'] == 'Consumable' and item['args'][0] is not None:
            object_list.append(Consumable(item['name'], item['description'], item['value'], item['args'][0]))
        else:
            object_list.append(False)
    
    return(object_list)

# def view_map(room, view_distance):
    # #Searches for room object in 2D list:
    # for i, row in enumerate(rooms):
        # for n, room in enumerate(row):
            # if player.room is room:
                # x_pos = n
                # org_x_pos = n
                # y_pos = i

    # for n in range(view_distance * 2 + 1):
        # x_pos = org_x_pos
        # falsed = 0
        # for i in range(view_distance):
            # if rooms[y_pos][x_pos - 1] is not False:
                # x_pos -= 1
            # else:
                # falsed += 1

        # # for i in range(falsed):
            # # sys.stdout.write("  ")
        # # sys.stdout.write(" ")
        # # x_pos += falsed * 2
        # # sys.stdout.write(" " + map_icons[room.map_type])
        # # for i in range(view_distance * 2 + 1 - falsed):
            # # if x_pos < len(rooms[y_pos]) - 1:
                # # sys.stdout.write(" " + map_icons[rooms[y_pos][x_pos].map_type])
                # # x_pos += 1
            # # else:
                # # sys.stdout.write("  ")
        # for i in range(falsed):
            # sys.stdout.write("  ")
        # x_pos += falsed * 2
        # for i in range(view_distance * 2 + 1 - falsed):
            # if x_pos < len(rooms[y_pos]):
                # if rooms[y_pos][x_pos] is not False:
                    # sys.stdout.write(" " + map_icons[rooms[y_pos][x_pos].map_type])
                # else:
                    # sys.stdout.write("  ")
                # x_pos += 1
            # else:
                # break
        
        # print("")
        # if y_pos < len(rooms) - 1:
            # y_pos += 1
        # else:
            # break
        
    
directions = {'n': 'north', 'e': 'east', 's': 'south', 'w': 'west'}
#map_icons = {'building': '*', 'path': '+', 'player': 'X'}
#map_icons = {'path': '=', 'tailor': 'T', 'bank': '$', 'smith': '%', 'poi': 'x'}

# town_square = Town("Town Square", "A stone brick fountain is located in the middle. You see farmers selling their goods.")
# tailor = Town("Tailor", "You see sewing supplies in the back.")
# martins_way = [Town("Martin's Way 1", "A wide stone brick road."), Town("Martin's Way 2", "A wide stone brick road.")]
# blacksmith = Town("Blacksmith", "A little stone building. You feel the heat from the forge as soon as you step in.")
# north_gate = Wilderness("North Gate", "A high valved gate. Two guards are patrolling everyone coming in.", {}, Loot_table([{'name': 'Wolf', 'level':1, 'percent': 0.75}]))
# forest = Resource("Black Forest", "The trees are so tightly packed you can barely see sunlight.", {}, None, None)

monsters = [{'name': 'Wolf', 'max_hp': 25, 'hp_per_hit': 5}]

# tailor.doors['east'] = martins_way[1]
# town_square.doors['north'] = martins_way[0]
# town_square.doors = {'north': martins_way[0]}
# martins_way[0].doors['north'] = martins_way[1]
# martins_way[0].doors['south'] = town_square
# martins_way[1].doors['east'] = blacksmith
# martins_way[1].doors['south'] = martins_way[0]
# martins_way[1].doors['west'] = tailor
# martins_way[1].doors['north'] = north_gate
# north_gate.doors['south'] = martins_way[1]
# north_gate.doors['north'] = forest
# blacksmith.doors['west'] = martins_way[1]
# forest.doors['south'] = north_gate

# town_square.type = 'path'
# tailor.type = 'building'
# blacksmith.type = 'building'
# martins_way[0].type = 'path'
# martins_way[1].type = 'path'
# north_gate.type = 'building'
# forest.type = 'path'

# tailor.merchant = Merchant(1.0, 0.8)
# blacksmith.merchant = Merchant(1.0, 0.8)

# leather_jacket = Armour("Leather Jacket", "A large leather jacket. The quality isn't that good.", 5, 10)
# leather_pants = Armour("Leather Pants", "A pair of leather pants. The quality isn't that good.", 5, 10)
# iron_pickaxe = Weapon("Iron Pickaxe", "A simple iron pickaxe. Useful for mining", 10, 10)
# iron_sword = Weapon("Iron Sword", "A simple iron sword. Useful for slaying enemies", 15, 20)
# iron_axe = Weapon("Iron Axe", "A simple iron axe. Useful for cutting down trees", 10, 15)
# apple = Consumable("Apple", "A tasty apple", 3, 10)
# wood = Item("Log", "A heavy oak log. Useful for crafting.", 2)

# forest.item = wood
# forest.weapon_required = iron_axe

# tailor.merchant.add_item(leather_jacket)
# tailor.merchant.add_item(leather_pants)
# blacksmith.merchant.add_item(iron_pickaxe)
# blacksmith.merchant.add_item(iron_sword)
# blacksmith.merchant.add_item(iron_axe)
# tailor.merchant.add_item(apple)

#rooms = [[('Tailor', 'You see sewing supplies in the back', 'Town', ([leather_jacket, leather_pants, apple])), ("Martin's Way", 'A wide stone brick road', 'Town', ())]]

if not os.path.isfile("items.json"):
    print("No item file found.")
    sys.exit()

file = open("items.json", "r")
items = json.loads(file.read())
file.close()
items = convert_items(items)

if not os.path.isfile("world.json"):
    print("No world file found.")
    sys.exit()
    
file = open("world.json", "r")
rooms = json.loads(file.read())
file.close()
rooms = convert_rooms(rooms)
print(rooms)

town_square = rooms[0][1]

player = Player(town_square) #Starting room is always town square.

refresh = True
player.inventory.append(items[3])
player.inventory.append(items[4])

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
        #view_map(player.room, 4)
        print("")
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
        # print("")
        # player.view_equipment()
    elif walk_to == 'u' or walk_to == 'use':
        player.view_inventory(True)
        print("Enter number to use or equip.")
        use = input("~")
        if use.isdigit():
            use = int(use)
            if use >= 0 and use <= len(player.inventory) - 1 and len(player.inventory) > 0:
                if isinstance(player.inventory[use], Consumable):
                    if player.hp + player.inventory[use].hp_restore >= player.max_hp:
                        player.hp = player.max_hp
                        print("You were restored to " + str(player.max_hp) + " HP.")
                    else:
                        player.hp += player.inventory[use].hp_restore
                        print("You were restored to " + str(player.hp + player.inventory[use].hp_restore) + " HP.")
                    player.inventory.pop(use)
                elif isinstance(player.inventory[use], Armour): 
                    if player.inventory[use].level_required <= player.level:
                        player.armour.append(player.inventory[use]) #Appends value to equipment.
                        item = player.inventory.pop(use) #Removes value from inventory.
                        player.defense += item.defense
                        print("Equipped item.")
                        print("Your Defense level is " + str(player.defense))
                    else:
                        print("This item can not be used until level " + str(player.inventory[use].level_required) + ".")
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
                elif isinstance(player.inventory[use], Weapon) and isinstance(player.room, Resource):
                    if player.inventory[use] == player.room.weapon_required:
                        print("You got one " + player.room.item.name + ".")
                        player.inventory.append(player.room.item)
                    else:
                        print("You are not able to use this tool here.")
                else:
                    print("This item can not be equipped.")
            elif use - len(player.inventory) >= 0 and use - len(player.inventory) <= len(player.armour) and len(player.armour) > 0:
                player.inventory.append(player.armour[use - len(player.inventory)])
                item = player.armour.pop(use - len(player.inventory))
                player.defense -= item.defense
                print("You put your " + item.name + " in your inventory.")
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