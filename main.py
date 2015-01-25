import sys
import math
import json
import os.path

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
                    object_row.append(Resource(room['name'], room['description'], {}, room['args'][1], room['args'][2], room['map'])) #room['args'] represents arguments.
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
    
file = open("world.json", "r")
rooms = json.loads(file.read())
file.close()
rooms = convert_rooms(rooms)

town_square = rooms[0][1]

player = Player(town_square) #Starting room is always town square.

refresh = True
walk_to_left = []
player.inventory.append(items[3])
player.inventory.append(items[4])

if os.path.isfile("player.json"): #Loads save file.
    file = open("player.json")
    player_data = json.loads(file.read())
    file.close()
    for item in player_data['inventory']:
        player.inventory.append(items[item])
    for item in player_data['armour']:
        player.armour.append(items[item])
    player.money = player_data['gold']
    player.in_fight = player_data['in_fight']
    player.defense = player_data['defense']
    player.room = rooms[player_data['room'][0]][player_data['room'][1]]
    player.hp = player_data['hp']
    player.max_hp = player_data['max_hp']
    print("Save file loaded.")

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
        print("HP: " + str(player.hp))
        print("Defense: " + str(player.defense))
    elif walk_to == 'i' or walk_to == 'inventory':
        player.view_inventory()
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
    elif walk_to == 'm' or walk_to == 'map':
        refresh = True
    elif walk_to == 'q' or walk_to == 'quit':
        file_inventory = []
        file_armour = []
        for player_item in player.inventory:
            for i, item in enumerate(items):
                if player_item is item:
                    file_inventory.append(i)
        for player_armour in player.armour:
            for i, item in enumerate(items):
                if player_armour is item:
                    file_armour.append(i)
        for n, row in enumerate(rooms):
            for i, room in enumerate(row):
                if room is player.room:
                    file_room = [n, i]
        stats = {'hp': player.hp, 'gold': player.money, 'max_hp': player.max_hp, 'defense': player.defense, 'in_fight': player.in_fight, 'room': file_room, 'inventory': file_inventory, 'armour': file_armour}
        file = open("player.json", "w")
        file.write(json.dumps(stats, indent=4, separators=(',', ': ')))
        file.close()
        print("Saved game data.")
        sys.exit()
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