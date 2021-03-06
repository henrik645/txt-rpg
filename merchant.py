from item import Item

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

class Banker:
    def get_items(self, player):
        items_formatted = []
        bank_list = []
        for item, amount in player.bank.items():
            items_formatted.append((item.name, amount))
            bank_list.append(item)
        
        return items_formatted, bank_list
    
    def add_item(self, player, item):
        if (not isinstance(item, Item)):
            raise TypeError("Unexpected " + type(item))
        
        if item in player.bank:
            player.bank[item] += 1
        else:
            player.bank[item] = 1
        
        return True
    
    def remove_item(self, player, item):
        if (not isinstance(item, Item)):
            raise TypeError("Unexpected " + type(item))
        
        if item in player.bank:
            if player.bank[item] == 1:
                player.bank.pop(item)
            else:
                player.bank[item] -= 0
            return True
        else:
            return False