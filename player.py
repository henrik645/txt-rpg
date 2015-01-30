class Player:
    def __init__(self, room, hp=100, max_hp=100, defense=0, money=100, inventory=[], armour={"gloves": None, "shirt": None, "pants": None, "boots": None, "right": None, "left": None, "both": None}, killed=False, in_fight=False, level=1):
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
            if_run = True
            items_formatted = []
            
            for item in self.inventory:
                items_formatted.append((item[1].name, item[0]))
            
            print("  - Inventory -  ")
            
            count = 0
            if use_menu:
                for item in items_formatted:
                    if item[1] > 1:
                        print(" " + str(count) + " " + item[0] + " (" + str(item[1]) + "x)")
                    else:
                        print(" " + str(count) + " " + item[0])
                    count += 1
            else:
                for item in items_formatted:
                    if item[1] <= 1:
                        print(" * " + item[0])
                    else:
                        print(" * " + item[0] + " (" + str(item[1]) + "x)")
        else:
            if_run = False
        items_formatted = []
        item_list = []
        for item in self.armour.values():
            if item is not None:
                items_formatted.append(item.name)
                item_list.append((item.slot, item))
            
        if len(items_formatted) > 0:
            if2_run = True
            if if_run:
                print("")
            print("  - Equipment -  ")
            
            if use_menu:
                for i, item in enumerate(items_formatted):
                    print(" " + str(i + len(self.inventory)) + " " + item)
            else:
                for item in items_formatted:
                    print(" * " + item)
        
            return item_list
        else:
            if2_run = False
        if if_run == False and if2_run == False:
            print("You do not have any items in your inventory.")
        
    def append_to_inventory(self, append_item):
        for player_item in self.inventory:
            if append_item.name == player_item[1].name and append_item.description == player_item[1].description and append_item.value == player_item[1].value:
                player_item[0] += 1
                break
        else:
            self.inventory.append([1, append_item])
    
    def pop_from_inventory(self, pop_int):
        if self.inventory[pop_int][0] <= 1:
            item = self.inventory.pop(pop_int)
        else:
            self.inventory[pop_int][0] -= 1
            item = self.inventory[pop_int]
        return item[1]