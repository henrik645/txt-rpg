import os.path
import json
import sys

types = ["Town", "Resource", "Wilderness"]

world_file = input("Enter world file: ")
if not os.path.isfile(world_file):
    create_file = input(world_file + " not found. Create file [y/n]?")
    if create_file == "y" or create_file == "yes":
        file = open(world_file, "w")
        file.write("{}")
        file.close()
    else:
        sys.exit()

file = open(world_file)
rooms = json.loads(file.read())
file.close()

while True:
    sys.stdout.write("  ")
    for i in range(len(rooms[1])):
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
            if command == "i":
                rooms.insert(line + 1, [])
            else:
                rooms.insert(line, [])
            for i in range(len(rooms[1])):
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
                    print(item)
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
            if input("Add merchant? ") == "y":
                merchant_items = []
                while True:
                    merchant_item = input("Enter item ID: ")
                    if merchant_item == "":
                        break
                    merchant_items.append(merchant_item)
                args[0] = merchant_items
                
            current_room['name'] = name
            current_room['description'] = description
            current_room['type'] = type
            current_room['args'] = args
            current_room['map'] = 'wilderness'