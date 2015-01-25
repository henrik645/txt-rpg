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