import os.path
import json
import sys

types = ["Town", "Resource", "Wilderness"]
item_types = ["Weapon", "Armour", "Consumable", "Item"]
slot_types = ["gloves", "shirt", "pants", "boots", "right", "left", "both"]

world_file = input("Enter world file: ")
item_file = input("Enter item file: ")
crafting_file = input("Enter crafting file: ")
if not os.path.isfile(world_file):
    create_file = input(world_file + " not found. Create file [y/n]?")
    if create_file == "y" or create_file == "yes":
        file = open(world_file, "w")
        file.write('[\n\t[\n\t\t{\n\t\t\t"name": false\n\t\t}\n\t]\n]')
        file.close()
    else:
        sys.exit()

if not os.path.isfile(item_file):
    create_file = input(item_file + " not found. Create file [y/n]?")
    if create_file == "y" or create_file == "yes":
        file = open(item_file, "w")
        file.write("{}")
        file.close()
    else:
        sys.exit()

if not os.path.isfile(crafting_file):
    create_file = input(crafting_file + " not found. Create file [y/n]?")
    if create_file == "y" or create_file == "yes":
        file = open(crafting_file, "w")
        file.write("[]")
        file.close()
    else:
        sys.exit()

file = open(world_file)
rooms = json.loads(file.read())
file.close()

file = open(item_file)
items = json.loads(file.read())
file.close()

file = open(crafting_file)
crafting = json.loads(file.read())
file.close()

while True:
    sys.stdout.write("  ")
    for i in range(len(rooms[0])):
        sys.stdout.write(str(i) + " ")
    print(" ")
    for i, row in enumerate(rooms):
        sys.stdout.write(str(i))
        for room in row:
            if room['name'] is not False:
                sys.stdout.write(" *")
            else:
                sys.stdout.write("  ")
        print(" ")

    print(" ")
    
    command = input("?")
    if command.lower() == "i":
        
        line = input("~")
        line = int(line)
        if line <= len(rooms):
            room_width = len(rooms[0])
            if command == "i":
                rooms.insert(line + 1, [])
                for i in range(len(rooms[0])):
                    rooms[line + 1].append({"name": False})
            else:
                rooms.insert(line, [])
                for i in range(len(rooms[0])):
                    rooms[line].append({"name": False})
            # for i in range(len(rooms[line])):
                # name = input("Name: ")
                # if name != "":
                    # description = input("Desc: ")
                    # print("")
                    # print("1: Town")
                    # print("2: Resource")
                    # print("3: Wilderness")
                    # print("-------------")
                    # type = input("Type: ")
                    # type = types[int(type)]
                    # args = []
                    # if command == "i":
                        # rooms[line + 1].insert(i, {'name': name, 'description': description, 'type': type, 'args': args, 'map': 'wilderness'})
                    # else:
                        # rooms[line].insert(i, {'name': name, 'description': description, 'type': type, 'args': args, 'map': 'wilderness'})
                # else:
                    # if command == "i":
                        # rooms[line + 1].insert(i, {'name': False})
                    # else:
                        # rooms[line].insert(i, {'name': False})
    elif command.lower() == "s":
        file = open(world_file, "w")
        json_rooms = json.dumps(rooms, indent=4, separators=(',', ': '))
        file.write(json_rooms)
        file.close()
        file = open(item_file, "w")
        json_items = json.dumps(items, indent=4, separators=(',', ': '))
        file.write(json_items)
        file.close()
        file = open(crafting_file, "w")
        json_crafting = json.dumps(crafting, indent=4, separators=(',', ': '))
        file.write(json_crafting)
        file.close()
        print("File saved.")
    elif command.lower() == "q":
        print("Quitting...")
        sys.exit()
    elif command.lower() == "c":
        line = input("~")
        line = int(line)
        if command == "c":
            for row in rooms:
                row.insert(line + 1, {'name': False})
        else:
            for row in rooms:
                row.insert(line, {'name': False})
    elif command.lower() == "d":
        line = input("~")
        x_pos, y_pos = line.replace(' ', '').split(',') #strips away all spaces and makes it two strings, x and y.
        y_pos, x_pos = int(y_pos), int(x_pos)
        delete = input("Delete room at " + str(x_pos) + "," + str(y_pos) + "? ")
        if delete == 'y':
            rooms[y_pos][x_pos] = {'name': False}
    elif command.lower() == "r":
        line = input("~")
        y_pos = int(line)
        if input("Delete row at " + str(y_pos) + "? ") == "y":
            if command == "r":
                for x_pos in range(len(rooms[y_pos])):
                    rooms[y_pos][x_pos] = {'name': False}
            else:
                rooms.pop(y_pos)
    elif command.lower() == "x":
        line = input("~")
        line = int(line)
        if input("Delete column at " + str(line) + "? ") == "y":
            if command == "x":
                for y_pos in range(len(rooms)):
                    rooms[y_pos][line] = {'name': False}
            else:
                for y_pos in range(len(rooms)):
                    rooms[y_pos].pop(line)
    elif command.lower() == 'l':
        print("List of items: ")
        for i, item in enumerate(items):
            print(str(i) + ": " + item['name'])
        item = input("~")
        if item != "":
            if item == "a":
                items.append({'name': False})
                item = len(items) - 1
            if item == "d":
                delete_item = input("~")
                if input("Delete item " + items[int(delete_item)]['name'] + " [y/n]? ") == "y":
                    items.pop(int(delete_item))
                    for i, craft in enumerate(crafting):
                        if craft['output'] == int(delete_item):
                            crafting.pop(i)
            else:
                if items[int(item)]['name'] is not False:
                    print("Name: " + items[int(item)]['name'])
                    print("Desc: " + items[int(item)]['description'])
                    print("Value: " + str(items[int(item)]['value']))
                    print("Type: " + items[int(item)]['type'])
                    if items[int(item)]['type'] == "Weapon":
                        print("Damage: " + str(items[int(item)]['args'][0]))
                    elif items[int(item)]['type'] == "Armour":
                        print("Defense: " + str(items[int(item)]['args'][0]))
                        print("Level: " + str(items[int(item)]['args'][1]))
                        print("Slot: " + str(items[int(item)]['slot']))
                    elif items[int(item)]['type'] == "Consumable":
                        print("HP-Restore: " + str(items[int(item)]['args'][0]))
                    printed_header = False
                    for craft in crafting:
                        if craft['output'] == int(item):
                            if printed_header == False:
                                printed_header = True
                                print("Crafting this item: ")
                            print("")
                            print("Item 1: " + str(craft['input'][0]))
                            print("Item 2: " + str(craft['input'][1]))
                            break
                            
                    print("")
                if input("Edit? ") == "y":
                    name = input("Name: ")
                    description = input("Description: ")
                    value = input("Value: ")
                    print("")
                    print("1. Weapon")
                    print("2. Armour")
                    print("3. Consumable")
                    print("4. Item")
                    print("-------------")
                    type = input("Type: ")
                    type = item_types[int(type) - 1]
                    if name == "":
                        name = items[int(item)]['name']
                    if description == '':
                        description = items[int(item)]['description']
                    if value == '':
                        value = items[int(item)]['value']
                    if type == '':
                        type = items[int(item)]['type']
                    if type == "Weapon":
                        damage = input("Damage: ")
                        args = [int(damage)]
                    elif type == "Consumable":
                        hp_restore = input("HP-Restore: ")
                        args = [int(hp_restore)]
                    elif type == "Armour":
                        defense = input("Defense: ")
                        level_required = input("Level: ")
                        args = [int(defense), int(level_required)]
                        print("")
                        print("1. Gloves")
                        print("2. Shirt")
                        print("3. Pants")
                        print("4. Boots")
                        print("5. Right")
                        print("6. Left")
                        print("7. Both")
                        print("-------------")
                        slot = input("Slot: ")
                        slot = slot_types[int(slot) - 1]
                    elif type == "Item":
                        args = []
                    if type == "Armour":
                        items[int(item)] = {'name': name, 'description': description, 'value': float(value), 'slot': slot, 'type': type, 'args': args}
                    else:
                        items[int(item)] = {'name': name, 'description': description, 'value': float(value), 'type': type, 'args': args}
                    if input("Crafted [y/n]? ") == "y":
                        while True:
                            item1 = input("Item 1: ")
                            if item1 == "":
                                break
                            item2 = input("Item 2: ")
                            crafting.append({"input": [item1, item2], "output": int(item)})
    else:
        x_pos, y_pos = command.replace(' ', '').split(',') #Strips away all spaces and makes it two strings, x and y.
        x_pos = int(x_pos) #Turns the strings
        y_pos = int(y_pos) #into integers.

        current_room = rooms[y_pos][x_pos]
        if current_room['name'] is not False:
            print("Name: " + current_room['name'])
            print("Desc: " + current_room['description'])
            print("Type: " + current_room['type'])
            if current_room['args'][0] != []:
                print("Merchant items: ")
                for item in current_room['args'][0]:
                    print(str(item) + ": " + items[item]['name'])
            if current_room['banker'] == True:
                print("A banker is added.")
            if current_room['type'] == "Wilderness":
                print("Monster table: ")
                for monster in current_room['args'][1]:
                    print("---------------")
                    print("Name: " + monster['name'])
                    print("Level: " + str(monster['level']))
                    print("Percent: " + str(monster['percent']))
            elif current_room['type'] == "Resource":
                print("Item: " + str(current_room['args'][1]))
                print("Required: " + str(current_room['args'][2]))
            print("")
        if input("Edit? ") == "y":
            name = input("Name: ")
            description = input("Desc: ")
            print("")
            print("1: Town")
            print("2: Resource")
            print("3: Wilderness")
            print("-------------")
            type = input("Type: ")
            if type == "":
                type = current_room['type']
            else:
                type = types[int(type) - 1]
            if name == "":
                name = current_room['name']
            if description == "":
                description = current_room['description']
            if type == "":
                type = current_room['type']
            if type == "Wilderness":
                print("Enter monsters:")
                monsters = []
                while True:
                    monster_name = input("Name: ")
                    if monster_name == "":
                        break
                    monster_level = input("Level: ")
                    monster_percent = input("Percent: ")
                    monsters.append({'name': monster_name, 'level': int(monster_level), 'percent': float(monster_percent)})
                args = [[], monsters]
            elif type == "Town":
                args = [[]]
            elif type == "Resource":
                item = input("Enter item ID: ")
                required = input("Enter tool ID: ")
                args = [[], item, required]
            input_y = input("Add merchant? ")
            if input_y == "y":
                merchant_items = []
                for i, item in enumerate(items):
                    print(str(i) + ": " + item['name'])
                while True:
                    merchant_item = input("Enter item ID: ")
                    if merchant_item == "":
                        break
                    merchant_items.append(int(merchant_item))
                args[0] = merchant_items
            elif input_y == "n":
                current_room['args'][0] = []
            input_y = input("Add banker? ")
            if input_y == "y":
                current_room['banker'] = True
            elif input_y == "n":
                current_room['banker'] = False
                
            current_room['name'] = name
            current_room['description'] = description
            current_room['type'] = type
            current_room['args'] = args
            current_room['map'] = 'wilderness'