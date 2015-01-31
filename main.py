import sys
import math
import json
import os.path
import time

from room import Room, Town, Wilderness, Resource
from player import Player
from item import Item, Weapon, Armour, Consumable
from merchant import Merchant
from monster import Monster 
from loot_table import Loot_table

#Types of items are: Item (Normal item), Consumable (Removed after use) and Armour (Normal armour. Defense level is stored at defense) If any item restores HP, the
#maximum amount of HP restored is stored at hp_restore
    
def view_selling_offers(merchant):
    selling_offers = merchant.merchant.get_selling_offers()

    selling_offers_formatted = []

    for offer in selling_offers:
        selling_offers_formatted.append((offer[0].name, offer[1]))

    for i in range(len(selling_offers_formatted)):
        print(str(i + 1) + " - " + selling_offers_formatted[i][0] + " - " + str(selling_offers_formatted[i][1]) + "G")

monster_percent_north_gate = [{'name': 'Wolf', 'level': 1, 'percent': 0.3}, {'name': 'Zombie' ,'level': 2, 'percent': 0.5}]

def convert_rooms(list):
    object_list = []
    for i, row in enumerate(list):
        object_row = []
        for n, room in enumerate(row):
            if room['name'] != False:
                if room['type'] == "Town":
                    object_row.append(Town(room['name'], room['description'], {}, room['map']))
                elif room['type'] == "Wilderness" and len(room['type']) >= 1:
                    object_row.append(Wilderness(room['name'], room['description'], {}, Loot_table(room['args'][1]), room['map'])) #room['args'] represents arguments.
                elif room['type'] == "Resource" and len(room['type']) >= 2:
                    object_row.append(Resource(room['name'], room['description'], {}, items[room['args'][1]], items[room['args'][2]], room['map'])) #room['args'] represents arguments.
                else:
                    object_row.append(False)
                if room['args'][0] != []:
                    object_row[n].merchant = Merchant(1.0, 0.8)
                    for item in room['args'][0]:
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
    
def convert_items(list):
    object_list = []
    for item in list:
        if item['type'] == 'Weapon' and item['args'][0] is not None:
            object_list.append(Weapon(item['name'], item['description'], item['slot'], item['args'][0], item['value']))
        elif item['type'] == 'Armour' and item['args'][0] is not None and item['args'][1] is not None:
            object_list.append(Armour(item['name'], item['description'], item['slot'], item['value'], item['args'][0], item['args'][1]))
        elif item['type'] == 'Item':
            object_list.append(Item(item['name'], item['description'], item['value']))
        elif item['type'] == 'Consumable' and item['args'][0] is not None:
            object_list.append(Consumable(item['name'], item['description'], item['value'], item['args'][0]))
        else:
            object_list.append(False)
    
    return(object_list)

def convert_crafts(list, items):
    object_list = []
    for item in list:
        item['output'] = items[item['output']]
        object_input = []
        for input_item in item['input']:
            input_item = items[input_item]
            object_input.append(input_item)
        object_list.append({'output': item['output'], 'input': object_input})
    return object_list

def monster_hp(level):
    monster_hp_level = math.floor((level / 2) ** 2 + 20)
    return monster_hp_level
    
def monster_hp_per_hit(level):
    monster_hp_hit = math.floor(((level / 2) ** 2 + 10 / 2))
    return monster_hp_hit

def monster_xp(level):
    monster_xp_level = math.floor((level / 2) ** 2 + 100)
    return monster_xp_level

def player_xp(level):
    level += 1 # +1 Since this is the xp required for the next level.
    player_xp_required = math.floor((level ** 2 + 100))
    return player_xp_required
    
def player_hp(level):
    player_hp_level = math.floor((level / 2) ** 2 + 25)
    return player_hp_level
    
directions = {'n': 'north', 'e': 'east', 's': 'south', 'w': 'west'}

monsters = [{'name': 'Wolf', 'max_hp': 25, 'hp_per_hit': 5}]

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

if not os.path.isfile("crafting.json"):
    print("No crafting file found.")
    sys.exit()

file = open("crafting.json", "r")
crafting = json.loads(file.read())
file.close()

crafting = convert_crafts(crafting, items)
    
file = open("world.json", "r")
rooms = json.loads(file.read())
file.close()
rooms = convert_rooms(rooms)

town_square = rooms[2][5]

player = Player(town_square) #Starting room is always town square.

refresh = True
walk_to_left = []
# player.append_to_inventory(items[3])
# player.append_to_inventory(items[4])

if os.path.isfile("player.json"): #Loads save file.
    file = open("player.json")
    player_data = json.loads(file.read())
    file.close()
    for item, number in player_data['inventory'].items():
        for z in range(number):
            player.append_to_inventory(items[int(item)])
    for key, item in player_data['armour'].items():
        if item is not None:
            player.armour[key] = items[item]
        else:
            player.armour[key] = None
    player.money = player_data['gold']
    player.in_fight = player_data['in_fight']
    player.defense = player_data['defense']
    player.room = rooms[player_data['room'][0]][player_data['room'][1]]
    player.hp = player_data['hp']
    player.max_hp = player_data['max_hp']
    player.level = player_data['level']
    player.xp = player_data['xp']
    print("Save file loaded.")
    time.sleep(0.5)

while True:
    if player.xp >= player_xp(player.level):
        print("You leveled up to level " + str(player.level + 1) + "!")
        player.level += 1
        player.xp -= player_xp(player.level)
        player.max_hp = player_hp(player.level)
        player.hp = player.max_hp
        print("Max HP: " + str(player.max_hp))
        
    if player.killed:
        player.killed = False
        player.go_to_room(town_square) #Town square is respawn point
        player.hp = player.max_hp
        print("You respawned at " + player.room.name + ".")
        time.sleep(2)
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
                        fight_monster = Monster(chosen_monster['name'], monster_hp(chosen_monster['level']), monster_hp_per_hit(chosen_monster['level']))
        elif isinstance(player.room, Resource):
            print("")
            print("Some " + player.room.item.name.lower() + " can be acquired here.")
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
    if walk_to_left == []:
        walk_to = input(">")
        walk_to = walk_to.lower()
        if len(walk_to) > 1:
            for char in walk_to[1:]:
                walk_to_left.append(char)
            walk_to = walk_to[:1]
    else:
        walk_to = walk_to_left.pop(0)
    if walk_to == 'g' or walk_to == 'gold':
        print("Gold: " + str(player.money))
        print("HP: " + str(player.hp) + " / " + str(player.max_hp))
        print("Defense: " + str(player.defense))
        print("Level: " + str(player.level))
        print("XP: " + str(player.xp) + " / " + str(player_xp(player.level)))
    elif walk_to == 'i' or walk_to == 'inventory':
        player.view_inventory()
    elif walk_to == 'u' or walk_to == 'use':
        armour_list = player.view_inventory(True)
        print("Enter number to use or equip.")
        use = input("~")
        if use.isdigit():
            use = int(use)
            if use >= 0 and use <= len(player.inventory) - 1 and len(player.inventory) > 0:
                if isinstance(player.inventory[use][1], Consumable):
                    if player.hp + player.inventory[use][1].hp_restore >= player.max_hp:
                        player.hp = player.max_hp
                        print("You were restored to " + str(player.max_hp) + " HP.")
                    else:
                        player.hp += player.inventory[use][1].hp_restore
                        print("You were restored to " + str(player.hp) + " HP.")
                    player.pop_from_inventory(use)
                elif isinstance(player.inventory[use][1], Armour): 
                    if player.inventory[use][1].level_required <= player.level:
                        if player.armour[player.inventory[use][1].slot] is None:
                            player.armour[player.inventory[use][1].slot] = player.inventory[use][1]
                            item = player.pop_from_inventory(use) #Removes value from inventory.
                            player.defense += item.defense
                            print("Equipped item.")
                            print("Your Defense level is " + str(player.defense))
                        else:
                            print("You are already wearing " + player.inventory[use][1].slot + ".")
                        #player.armour.append(player.inventory[use][1]) #Appends value to equipment.
                    else:
                        print("This item can not be used until level " + str(player.inventory[use][1].level_required) + ".")
                elif isinstance(player.inventory[use][1], Weapon) and player.in_fight:
                    print("You hit the " + fight_monster.name + " with your " + player.inventory[use][1].name + "!")
                    fight_monster.hp -= player.inventory[use][1].damage
                    if fight_monster.hp <= 0:
                        print("The " + fight_monster.name + " died!")
                        print("")
                        player.in_fight = False
                        xp_gained = monster_xp(chosen_monster['level'])
                        player.xp += xp_gained
                        print("You gained " + str(xp_gained) + " XP.")
                    else:                        
                        print(fight_monster.name + " HP: " + str(fight_monster.hp) + " / " + str(fight_monster.max_hp))
                        print("The " + fight_monster.name + " hit you!")
                        player.hp -= fight_monster.hp_per_hit - player.defense * 0.10
                        if player.hp <= 0:
                            print("The " + fight_monster.name + " killed you!")
                            player.in_fight = False
                            player.killed = True
                        else:
                            print("Your HP: " + str(player.hp) + " / " + str(player.max_hp))
                elif isinstance(player.inventory[use][1], Weapon) and isinstance(player.room, Resource):
                    if player.inventory[use][1] == player.room.weapon_required:
                        sys.stdout.write("You swing your " + player.inventory[use][1].name)
                        sys.stdout.flush()
                        for i in range(3):
                            sys.stdout.write(".")
                            sys.stdout.flush()
                            time.sleep(0.75)
                        print("")
                        print("You got one " + player.room.item.name + ".")
                        player.append_to_inventory(player.room.item)
                    else:
                        print("You are not able to use this tool here.")
                else:
                    print("This item can not be equipped.")
            elif use - len(player.inventory) >= 0 and use - len(player.inventory) <= len(player.armour) and len(player.armour) > 0:
                player.append_to_inventory(armour_list[use - len(player.inventory)][1])
                item = armour_list[use - len(player.inventory)][1]
                player.armour[armour_list[use - len(player.inventory)][0]] = None
                player.defense -= item.defense
                print("You put your " + item.name + " in your inventory.")
    elif walk_to == 'm' or walk_to == 'map':
        refresh = True
    elif walk_to == 'q' or walk_to == 'quit':
        file_inventory = {}
        file_armour = {}
        for player_item in player.inventory:
            for i, item in enumerate(items):
                if player_item[1] is item:
                    file_inventory[i] = player_item[0]
        for key, player_armour in player.armour.items():
            for i, item in enumerate(items):
                if player_armour is item:
                    file_armour[key] = i
                    break
                else:
                    file_armour[key] = None
        for n, row in enumerate(rooms):
            for i, room in enumerate(row):
                if room is player.room:
                    file_room = [n, i]
        stats = {'hp': player.hp, 'gold': player.money, 'max_hp': player.max_hp, 'defense': player.defense, 'in_fight': player.in_fight, 'room': file_room, 'inventory': file_inventory, 'armour': file_armour, "level": player.level, 'xp': player.xp}
        file = open("player.json", "w")
        file.write(json.dumps(stats, indent=4, separators=(',', ': ')))
        file.close()
        print("Saved game data.")
        sys.exit()
    elif walk_to == 'c' or walk_to == 'craft':
        player.view_inventory(True)
        print("")
        print("Combine items: ")
        item1_raw = input("Item 1: ")
        if item1_raw != "":
            item2_raw = input("Item 2: ")
            if isinstance(item1_raw, int) and isinstance(item2_raw, int):
                item1 = player.inventory[int(item1_raw)][1]
                item2 = player.inventory[int(item2_raw)][1]
                for craft in crafting:
                    if (item1 == craft['input'][0] and item2 == craft['input'][1]) or (item1 == craft['input'][1] and item2 == craft['input'][0]):
                        player.pop_from_inventory(int(item1_raw))
                        player.pop_from_inventory(int(item2_raw))
                        player.append_to_inventory(craft['output'])
                        print("Crafted one " + craft['output'].name + ".")
                        break
                else:
                    print("There are no recipies matching your items.")
    else:
        for dir_abbr, direction in directions.items():
            if direction in player.room.doors:
                if walk_to == dir_abbr and player.in_fight == False:
                    player.go_to_room(player.room.doors[direction])
                    if len(walk_to_left) <= 0:
                        refresh = True
                    break
                elif walk_to.lower() == direction and player.in_fight == False:
                    player.go_to_room(player.room.doors[direction])
                    if len(walk_to_left) <= 0:
                        refresh = True
                    break
                elif player.in_fight:
                    if len(walk_to_left) == 0: #If player is "running" through, the message will not be displayed, but just the attack message.
                        print("You can not leave while in a fight!")
                    break
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
                    player.append_to_inventory(selling_offers[walk_to][0])
            else:
                print("You cannot find this item in this store.")
        except:
            pass