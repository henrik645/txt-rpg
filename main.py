import sys
import math
import json
import os.path
import time

from room import Room, Town, Wilderness, Resource
from player import Player
from item import Item, Weapon, Armour, Consumable
from merchant import Merchant, Banker
from monster import Monster 
from loot_table import Loot_table
from quests import Quest

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
                
                if room['banker'] != False:
                    object_row[n].banker = Banker()
                
                if 'quests' in room:
                    object_row[n].quests = []
                    for i, quest in enumerate(room['quests']):
                        object_row[n].quests.append(quests[room['quests'][i]])
                
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
            object_list.append(Weapon(item['name'], item['description'], item['slot'], item['args'][0], item['value'], item['args'][1]))
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

def convert_quests(list, items):
    object_list = []
    
    for quest in list:
        quest_name = quest['name']
        quest_dialogue = quest['dialogue']
        quest_decline = quest['decline']
        quest_level = quest['level']
        
        object_steps = []
        for n, step in enumerate(quest['steps']):
            if 'item' in step or 'dialogue' in step or 'complete' in step:
                object_steps.append({})
            if 'item' in step:
                for i, item, amount in enumerate(items.items()):
                    if step['item'] == i:
                        object_steps[n]['item'][item] = amount
                        break
                else:
                    raise KeyError("No item with id " + str(step['item']) + " found.")
            if 'dialogue' in step:
                object_steps[n]['dialogue'] = step['dialogue']
            if 'complete' in step:
                object_steps[n]['complete'] = True
        
        object_rewards = []
        for n, reward in enumerate(rewards):
            if reward['type'] == 'items':
                for reward_item, amount in rewards['values'].items():
                    for i, item in enumerate(items):
                        if reward_item == i:
                            object_rewards[n]['items'][item] = amount
                            break
                else:
                    raise KeyError("No item with id " + str(step['item']) + " found.")
            elif reward['type'] == "xp":
                object_rewards['xp'] = reward['values']
            elif reward['type'] == "gold":
                object_rewards['gold'] = reward['values']
                    
        
        quest_steps = object_steps
        quest_rewards = object_rewards
        
        object = Quest(quest_name, quest_dialogue, quest_decline, quest_level, quest_steps, quest_rewards)
        object_list.append(object)
    
    return object_list

def monster_hp(level):
    monster_hp_level = math.floor((level * 1.2) ** 2 + 20)
    return monster_hp_level
    
def monster_hp_per_hit(level):
    monster_hp_hit = math.floor(((level / 2) ** 2 + 10))
    return monster_hp_hit

def monster_xp(level):
    monster_xp_level = math.floor((level * 2) ** 2 + 25)
    return monster_xp_level

def player_xp(level):
    level += 1 # +1 Since this is the xp required for the next level.
    player_xp_required = math.floor((level * 5) ** 2 + 100)
    return player_xp_required
    
def player_hp(level):
    player_hp_level = math.floor((level * 1.3) ** 2 + 25)
    return player_hp_level
    
directions = {'n': 'north', 'e': 'east', 's': 'south', 'w': 'west'}

#monsters = [{'name': 'Wolf', 'max_hp': 25, 'hp_per_hit': 5}, {'name': 'Scorpion', 'max_hp': 25, 'hp_per_hit': 5}]

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

if not os.path.isfile("quests.json"):
    print("No quests file found.")
    sys.exit()

file = open("crafting.json", "r")
crafting = json.loads(file.read())
file.close()

crafting = convert_crafts(crafting, items)

file = open("quests.json", "r")
quests = json.loads(file.read())
file.close()

quests = convert_quests(quests, items)
for quest in quests:
    print(quest.get_dialogue())
    while quest.advance_step():
        print(quest.get_dialogue())
    print(quest.decline)
sys.exit()

file = open("world.json", "r")
rooms = json.loads(file.read())
file.close()
rooms = convert_rooms(rooms)

town_square = rooms[2][5]

#town_square.banker = Banker()

player = Player(town_square) #Starting room is always town square.

refresh = True
map_refresh = False
walk_to_left = []
# player.append_to_inventory(items[3])
# player.append_to_inventory(items[4])

#player.bank[items[4]] = 1

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
    for item, number in player_data['bank'].items():
        item = items[int(item)]
        player.bank[item] = number
    player.money = player_data['gold']
    player.in_fight = player_data['in_fight']
    player.defense = player_data['defense']
    player.room = rooms[player_data['room'][0]][player_data['room'][1]]
    player.hp = player_data['hp']
    #player.max_hp = player_data['max_hp']
    player.level = player_data['level']
    player.max_hp = player_hp(player.level)
    player.xp = player_data['xp']
    print("Save file loaded.")
    time.sleep(0.5)
else:
    player.hp = player_hp(player.level)
    player.max_hp = player_hp(player.level)

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
        if player.in_fight:
            print("")
            print("You are battling a level " + str(chosen_monster['level']) + " " + fight_monster.name + ".")
            print("")
            print("Your HP: " + str(player.hp) + " / " + str(player.max_hp))
            print(fight_monster.name + " HP: " + str(fight_monster.hp) + " / " + str(fight_monster.max_hp))
        if isinstance(player.room, Wilderness) and map_refresh == False:
            chosen_monster = player.room.monster_percent.choose_from_list()
            if chosen_monster is not None:
                print("You have been attacked by a level " + str(chosen_monster['level']) + " " + str(chosen_monster['name']) + "!")
                player.in_fight = True
                fight_monster = Monster(chosen_monster['name'], monster_hp(chosen_monster['level']), monster_hp_per_hit(chosen_monster['level']))
        elif isinstance(player.room, Resource):
            print("")
            print("Some " + player.room.item.name.lower() + " can be acquired here.")
        if hasattr(player.room, 'merchant') and not player.in_fight:
            print("")
            print("A merchant is present.")
            view_selling_offers(player.room)
            print("Enter number to buy.")
            print("")
            print("You have " + str(player.money) + " G left.")
        if hasattr(player.room, 'banker') and not player.in_fight:
            print("")
            print("A banker is present.")
        if hasattr(player.room, 'quests') and not player.in_fight:
            for quest in player.room.quests:
                if not (quest in player.active_quests or quest in player.finished_quests):
                    print("")
                    print("There are quests available.")
                    break
        if not player.in_fight:
            print("")
            print("Exits:")
            for exit in player.room.doors:
                print(exit.title() + " (" + player.room.doors[exit].name + ")")
    map_refresh = False
    if walk_to_left == []:
        walk_to = input(">")
        walk_to = walk_to.lower()
        if len(walk_to) > 1:
            for char in walk_to[1:]:
                walk_to_left.append(char)
            walk_to = walk_to[:1]
    else:
        walk_to = walk_to_left.pop(0)
        # if len(walk_to_left) <= 0:
            # refresh = True
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
                # elif isinstance(player.inventory[use][1], Weapon) and player.in_fight:
                    # print("You hit the " + fight_monster.name + " with your " + player.inventory[use][1].name + "!")
                    # fight_monster.hp -= player.inventory[use][1].damage
                    # if fight_monster.hp <= 0:
                        # print("The " + fight_monster.name + " died!")
                        # print("")
                        # player.in_fight = False
                        # xp_gained = monster_xp(chosen_monster['level'])
                        # player.xp += xp_gained
                        # print("You gained " + str(xp_gained) + " XP.")
                    # else:                        
                        # print(fight_monster.name + " HP: " + str(fight_monster.hp) + " / " + str(fight_monster.max_hp))
                        # print("The " + fight_monster.name + " hit you!")
                        # player.hp -= fight_monster.hp_per_hit - player.defense * 0.10
                        # if player.hp <= 0:
                            # print("The " + fight_monster.name + " killed you!")
                            # player.in_fight = False
                            # player.killed = True
                        # else:
                            # print("Your HP: " + str(player.hp) + " / " + str(player.max_hp))
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
                elif isinstance(player.inventory[use][1], Weapon):
                    if player.inventory[use][1].level_required <= player.level:
                        if player.armour[player.inventory[use][1].slot] is None:
                            player.armour[player.inventory[use][1].slot] = player.inventory[use][1]
                            item = player.pop_from_inventory(use) #Removes value from inventory.
                            print("Equipped item.")
                            print("Your Damage level is " + str(item.damage) + ".")
                        else:
                            print("You are already wearing this type of item.")
                    else:
                        print("This item can not be used until level " + str(player.inventory[use][1].level_required) + ".")
                else:
                    print("This item can not be equipped.")
            elif use - len(player.inventory) >= 0 and use - len(player.inventory) <= len(player.armour) and len(armour_list) > 0:
                item = armour_list[use - len(player.inventory)][1]
                player.append_to_inventory(armour_list[use - len(player.inventory)][1])
                player.armour[item.slot] = None
                if isinstance(item, Armour):
                    player.defense -= item.defense
                print("You put your " + item.name + " in your inventory.")
    elif walk_to == 'm' or walk_to == 'map':
        refresh = True
        map_refresh = True
    elif walk_to == 'q' or walk_to == 'quit':
        file_inventory = {}
        file_armour = {}
        file_bank = {}
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
        for item, number in player.bank.items():
            for i, item_items in enumerate(items):
                if item == item_items:
                    file_bank[i] = number
        stats = {'hp': player.hp, 'gold': player.money, 'max_hp': player.max_hp, 'defense': player.defense, 'in_fight': player.in_fight, 'room': file_room, 'inventory': file_inventory, 'armour': file_armour, "level": player.level, 'xp': player.xp, 'bank': file_bank}
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
            if item1_raw.isdigit() and item2_raw.isdigit():
                if int(item1_raw) <= len(player.inventory) and int(item2_raw) <= len(player.inventory):
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
    elif (walk_to == 'b' or walk_to == 'bank') and hasattr(player.room, 'banker'):
        while True:
            armour_list = player.view_inventory(True)
            if len(player.bank) > 0:
                print("")
                print("  - Bank items -  ")
            items_formatted, bank_list = player.room.banker.get_items(player)
            for i, item in enumerate(items_formatted):
                if item[1] > 1:
                    print(" " + str(i + len(player.inventory) + len(armour_list)) + " " + item[0] + " (" + str(item[1]) + "x)")
                else:
                    print(" " + str(i + len(player.inventory) + len(armour_list)) + " " + item[0])

            if len(player.bank) > 0:
                print("Enter number to withdraw or deposit or press enter when done.")
            else:
                print("Enter number to deposit or press enter when done.")
            
            item = input("~")
            if item == "":
                refresh = True
                break
            if item.isdigit():
                item = int(item)
                if item >= len(player.inventory) + len(armour_list): #Meaning that the player has chosen to withdraw an item.
                    item = item - (len(player.inventory) + len(armour_list))
                    item = bank_list[item]
                    if player.bank[item] > 1: #Meaning that it can be subtracted
                        amount_items = input("How many: ")
                        if amount_items.isdigit():
                            amount_items = int(amount_items)
                        else:
                            amount_items = 1
                        if player.bank[item] < amount_items:
                            amount_items = player.bank[item]
                        if player.bank[item] > amount_items:
                            player.bank[item] -= amount_items
                            for i in range(amount_items):
                                player.append_to_inventory(item)
                        else:
                            for i in range(player.bank[item]):
                                player.append_to_inventory(item)
                            player.bank.pop(item)
                    else: #Meaning we need to pop it entirely.
                        player.append_to_inventory(item)
                        player.bank.pop(item)
                    print("You withdrew your " + item.name + " and put it in your inventory.")
                elif item >= len(player.inventory):
                    print("You can not deposit directly from your equipment.")
                elif item < len(player.inventory):
                    item_inventory = player.inventory[item][1]
                    if player.inventory[item][0] > 1:
                        amount_items = input("How many: ")
                        if amount_items.isdigit():
                            amount_items = int(amount_items)
                        else:
                            amount_items = 1
                        if amount_items > player.inventory[item][0]:
                            amount_items = player.inventory[item][0]
                    if item_inventory in player.bank: #If item already is in bank, and this item can be stacked on top of that.
                        player.bank[item_inventory] += amount_items
                    else: #This item is new to this bank
                        player.bank[item_inventory] = amount_items
                    for i in range(amount_items):
                        player.pop_from_inventory(item)
                    print("You deposited your " + item_inventory.name + " to your bank account.")
                print("")
            refresh = False
    elif walk_to == "a" or walk_to == "attack":
        if player.armour['right'] is None:
            player.armour['right'] = items[8] #Items 8 is bare hands, which is a weapon only used internally.
        if player.in_fight:
            print("You hit the " + fight_monster.name + " with your " + player.armour['right'].name + "!")
            fight_monster.hp -= player.armour['right'].damage
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
        else:
            print("You can not attack while not in a fight.")
            
        if player.armour['right'] == items[8]:
            player.armour['right'] = None
    elif walk_to == 'p' or walk_to == 'quests':
        take_quests = []
        for quest in player.room.quests:
            if not (quest in player.active_quests or quest in player.finished_quests):
                take_quests.append(quest)
        if len(take_quests) <= 0:
            print("There are no available quests here.")
            print("")
        if len(player.active_quests) > 0 or len(player.finished_quests) > 0:
            if len(player.active_quests) > 0:
                print("Your active quests:")
                for quest in player.active_quests:
                    print(quest[0]['name'] + " (" + quest[0]['steps'][quest[1]]['description'] + ")")
                print("")
            if len(player.finished_quests) > 0:
                print("Your finished quests:")
                for quest in player.finished_quests:
                    print(quest['name'])
                print("")
        if len(take_quests) > 0:
            print("The following quests are available:")
            for i, quest in enumerate(take_quests):
                print(str(i) + ": " + quest['name'])
            print("")
            chosen_quest = input("~")
            if chosen_quest.isdigit():
                chosen_quest = int(chosen_quest)
            if chosen_quest != "" and chosen_quest < len(take_quests):
                chosen_quest = take_quests[chosen_quest]
                print(chosen_quest['dialogue'])
                print("")
                print("Reward:")
                for reward in chosen_quest['reward']:
                    if reward['type'] == "gold":
                        print("Gold: " + str(reward['values']))
                    elif reward['type'] == "xp":
                        print("XP: " + str(reward['values']))
                    elif reward['type'] == "items":
                        for item, amount in reward['values'].items():
                            if amount <= 1:
                                print(items[int(item)].name)
                            else:
                                print(items[int(item)].name + " (" + str(amount) + "x)")
                if input("Accept quest? ") == "y":
                    player.active_quests[chosen_quest] = 0
                    print("You accepted " + chosen_quest['name'] + ".")
                else:
                    print(chosen_quest['decline'])
            print("")
    else:
        for dir_abbr, direction in directions.items():
            if direction in player.room.doors:
                if walk_to == dir_abbr and player.in_fight == False:
                    player.go_to_room(player.room.doors[direction])
                    refresh = True
                    break
                elif walk_to.lower() == direction and player.in_fight == False:
                    player.go_to_room(player.room.doors[direction])
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