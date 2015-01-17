import sqlite3 as sqlite;
import time

conn = sqlite.connect("rpg.db")
c = conn.cursor()
def placeInfo(x, y):
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
  c.execute('SELECT desc FROM places WHERE x=? and y=?', (x, y))
  desc = c.fetchone()
  c.execute('SELECT exit FROM places WHERE x=? and y=?', (x, y))
  exits = c.fetchone()
  print (title[0][0])
  print (desc[0])
  print ("")
  print ("Exits: ")
  north = False
  east = False
  south = False
  west = False
  if exits[0] & 8 == 8:
    print("North (" + title[1][0] + ")")
    north = True
  if exits[0] & 4 == 4:
    print("East (" + title[3][0] + ")")
    east = True
  if exits[0] & 2 == 2:
    print("South (" + title[2][0] + ")")
    south = True
  if exits[0] & 1 == 1:
    print("West (" + title[4][0] + ")")
    west = True
  return (north, east, south, west)

  
x, y = 1, 1

while True:
  for i in range(30):
    print("")
  exits = False
  exits = placeInfo(x, y)
  action = raw_input(">")
  if action == "n" and exits[0]:
      y += 1
  elif action == "e" and exits[1]:
    x += 1
  elif action == "s" and exits[2]:
    y -= 1
  elif action == "w" and exits[3]:
    x -= 1
  else:
    print("No such command")
  print(x, y)