import sqlite3 as sqlite;
import time

global inventory
inventory = []
conn = sqlite.connect("rpg.db")
c = conn.cursor()

def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

def showInventory(use):
  print(armour)
  print(len(armour))
  print(" - Inventory - ")
  item_names = []
  item_descriptions = []
  for i in range(len(inventory)):
    c.execute('SELECT name FROM items WHERE id=?', (inventory[i],))
    item_names.append(c.fetchone())
  for i in range(len(inventory)):
    c.execute('SELECT description FROM items WHERE id=?', (inventory[i],))
    item_descriptions.append(c.fetchone())
  if len(inventory) <= 0:
    print("You are not in possession of any items.")
    return False
  else:
    if use == "show":
      for i in range(len(inventory)):
        print(item_names[i][0] + " - " + item_descriptions[i][0])
    else:
      for i in range(len(inventory)):
        print(str(i) + " - " + item_names[i][0] + " - " + item_descriptions[i][0])
    return True

def showEquipment():
  if len(armour) > 0:
    c.execute('SELECT name FROM items WHERE id=?', (armour[i],))
    item_names.append(c.fetchone())
    c.execute('SELECT description FROM items WHERE id=?', (armour[i],))
    print("")
    print("Equipment: ")
    if use == "use":
      for i in range(len(armour)):
        print(str(i + len(inventory)) + " - " + item_names[i][0] + " - " + item_descriptions[i][0])
    else:
      for i in range(len(armour)):
        print(item_names[i][0] + " - " + item_descriptions[i][0])
    return True
  else:
    print("You do not have any equipment.")
    return False

def placeInfo(x, y, refresh):
  title = ["", "", "", "", ""]
  c.execute('SELECT title FROM places WHERE x=? and y=?', (x, y))
  title[0] = c.fetchone()
  c.execute('SELECT title FROM places WHERE x=? and y=?', (x, y + 1))
  title[1] = c.fetchone()
  c.execute('SELECT title FROM places WHERE x=? and y=?', (x, y - 1))
  title[2] = c.fetchone()
  c.execute('SELECT title FROM places WHERE x=? and y=?', (x + 1, y))
  title[3] = c.fetchone()
  c.execute('SELECT title FROM places WHERE x=? and y=?', (x - 1, y))
  title[4] = c.fetchone()
  c.execute('SELECT description FROM places WHERE x=? and y=?', (x, y))
  description = c.fetchone()
  c.execute('SELECT exit FROM places WHERE x=? and y=?', (x, y))
  exits = c.fetchone()
  c.execute('SELECT id FROM places WHERE x=? and y=?', (x, y)) #x, y -> place_ids
  place_ids = c.fetchone()
  c.execute('SELECT action FROM places_actions WHERE place_id=?', (place_ids[0],)) #actions = place_actions(place_ids)
  actions_available = c.fetchone()
  if actions_available is not None:
    if actions_available[0] == "buy":
      item_ids = []
      item_names = []
      item_descriptions = []
      item_prices = []
      c.execute('SELECT item_id FROM places_items WHERE place_id=?', (place_ids[0],)) #item_id = places_items(place-id)
      for i in c:
        item_ids.append(i[0])
      for i in range(len(item_ids)):
        c.execute('SELECT name FROM items WHERE id=?', (item_ids[i],))
        item_names.append(c.fetchone())
      for i in range(len(item_ids)):
        c.execute('SELECT description FROM items WHERE id=?', (item_ids[i],))
        item_descriptions.append(c.fetchone())
      c.execute('SELECT price FROM places_items WHERE place_id=?', (place_ids[0],))
      for i in c:
        item_prices.append(i)
  
  if refresh:
    print (title[0][0])
    print (description[0])
    print ("")
    print ("Exits: ")
  north = False
  east = False
  south = False
  west = False
  if exits[0] & 8 == 8:
    if refresh:
      print("North (" + title[1][0] + ")")
    north = True
  if exits[0] & 4 == 4:
    if refresh:
      print("East (" + title[3][0] + ")")
    east = True
  if exits[0] & 2 == 2:
    if refresh:
      print("South (" + title[2][0] + ")")
    south = True
  if exits[0] & 1 == 1:
    if refresh:
      print("West (" + title[4][0] + ")")
    west = True
  
  if refresh:
    print("")
    print ("Actions available: ")
    if actions_available is not None:
      for i in actions_available:
        print(i)
    else:
      print("None")
  if actions_available is not None:
    return (north, east, south, west, actions_available, item_ids, item_names, item_descriptions, item_prices)
  else:
    return(north, east, south, west, None, None, None, None, None)

x, y = 1, 1
gold = 5
refresh = True
maxhp = 100
hp = 70
defense = 0
armour = []

while True:
  if refresh:
    for i in range(30):
      print("")
  #print("")
  #print("")
  exits = None
  if refresh:
    north, east, south, west, actions_available, item_ids, item_names, item_descriptions, item_prices = placeInfo(x, y, True)
    refresh = False
  else:
    north, east, south, west, actions_available, item_ids, item_names, item_descriptions, item_prices = placeInfo(x, y, False)
  exits = [north, east, south, west]
  action = ""
  action = raw_input(">")
  action = action.lower()
  if (action == "n" or action == "north") and exits[0]:
    y += 1
    refresh = True
  elif (action == "e" or action == "east") and exits[1]:
    x += 1
    refresh = True
  elif (action == "s" or action == "south") and exits[2]:
    y -= 1
    refresh = True
  elif (action == "w" or action == "west") and exits[3]:
    x -= 1
    refresh = True
  elif (action == "g" or action == "gold"):
    print("You have: " + str(gold) + "G")
    print("HP: " + str(hp))
    print("Defense: " + str(defense))
  elif (action == "i" or action == "inventory"):
    showInventory("show")
    showEquipment()
  elif action == "u" or action == "use":
    if showInventory("use"):
      print("")
      itemUsed = raw_input("Use item: ")
      if is_int(itemUsed):
        item_id = inventory[int(itemUsed)]
        c.execute('SELECT hp_restore, attack, perishable, armour FROM item_stats WHERE item_id=?', (item_id,))
        stats = []
        for i in c:
          stats.append(i)
        if hp is not None and stats[0][0] is not None and (hp + stats[0][0]) < maxhp:
            hp += stats[0][0]
        elif hp is not None and stats[0][0] is not None and (hp + stats[0][0]) >= maxhp:
            hp = maxhp
        
        if stats[0][1] is not None:
          damage = stats[0][1]
        
        if stats[0][2] is not None:
          inventory.remove(inventory[int(itemUsed)])
          
        if stats[0][3] is not None:
          defense += stats[0][3]
          armour.append(inventory[int(itemUsed)])
          inventory.remove(inventory[int(itemUsed)])
  else:
    if actions_available is not None:
      for i in actions_available:
        if action == i:
          print("")
          for z in range(len(item_ids)):
            print(str(z) + " " + item_names[z][0] + " - " + item_descriptions[z][0] + " - " + str(item_prices[z][0]) + "G")
          chosen_item = raw_input("Enter item: ")
          if is_int(chosen_item):
            if int(chosen_item) < len(item_prices):
              if item_prices[int(chosen_item)][0] > gold:
                print("You are not in possession of enough gold.")
              else:
                inventory.append(item_ids[int(chosen_item)])
                print("")
                gold -= item_prices[int(chosen_item)][0]
                print("You have " + str(gold) + "G left.")
            else:
              print("Enter again.")
          else:
            print("Enter again.")
    else:
      print("No such command")