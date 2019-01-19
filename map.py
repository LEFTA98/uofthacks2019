from location import Location
from characters import Character
from item import Item
from char_actions import Attack, Action


#{"locations": {"cave": {"description": "You are in a dank place.",
#						"items": [],
#						"characters": []},
#				"forest": {"description": "You are in a lush place.",
#						"items": [],
#						"characters": []},
#				"castle": {"description": "You are in a castle.",
#						"items": [],
#						"characters": []}},
# "adjacencies": {"cave": ["forest", "castle"],
#				 "forest": ["castle", "cave"],
#				 "castle": ["forest", "cave"]},
# "start": "cave"}
# 
data = {}
start = None
 
#INIT LOCATIONS HERE
forest = Location("forest", "You are in a lush place.")
data["forest"] = forest
 
cave = Location("cave", "You are in a dank place.")
data["cave"] = cave

#ADD ITEMS HERE
#ADD CHARACTERS HERE
 
#DECLARE ADJACENCY HERE
data["forest"].add_adj(data["cave"])
data["cave"].add_adj(data["forest"])
 
#PUT START LOCATION HERE
start = data["forest"]