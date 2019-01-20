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
data["Clearing"] = Location("Clearing", "You are in a small, brightly-lit clearing.")

data["Crossroads"] = Location("Crossroads", "An old man stands at the corner of a road-bend.")

data["Pond of Healing"] = Location("Pond of Healing", "A luminous and still pond stands in the midst of the silence.")

data["Quezlat's Hill"] = Location("Quezlat's Hill", "A tent lies at the top of the rocky hill. Soulful voices penetrate the air.")

data["Rainbow Stream of Knowledge"] = Location("Rainbow Stream of Knowledge", "The stream glistens, a soft, familiar voice inviting you to venture closer.")

data["River of Lost"] = Location("River of Lost", "The river is covered with large scraps of garbage and plastic. It moves slowly, like thick glue.")

def temp(target):
    target.health+=2
#ADD ITEMS HERE
data["Clearing"].add_item(Item("mushrooms", "They are slightly bruised and dirty, but beggars can't be choosers.", True, False, temp, None))
def temp(target):
    target.health+=4
data["Clearing"].add_item(Item("flask", "Bruised and slightly discoloured, with strange white baubles glittering inside", True, False, temp, None))
data["Clearing"].add_item(Item("tissues", "A pile of white tissues. Weird.", False, False, None, None))
data["Clearing"].add_item(Item("body", "The body of a long-gone adventurer. His weapon seems to be missing.", False, False, None, None))
data["Clearing"].add_item(Item("chestplate", "The armour glitters with thick scales, but it has been used often. Its fabric is dirty and torn.", False, False, None, None))
def temp(target):
    target.health -=1
data["Clearing"].add_item(Item("sword", "A simple longsword, rusted with disrepair.", False, True, temp, None))
#ADD CHARACTERS HERE
goblin = Character("goblin", 2, False, "A small goblin. He seems extremely oblivious, but will attack if provoked.")
goblin.add_attack(Attack(1, "The goblin swipes at you!"))
data["Clearing"].add_character(goblin)

data["Crossroads"].add_character(Character("Guide of Astralon", 10, False, "A man materializes in thin air on the road-bend. He's wearing a golden cloak and his long beard floats over his thin locket. There's a soft halo around the ground on which he stands. You can ask him for advice if you wish."))
data["Pond of Healing"].add_character(Character("Tikki", 5, True, "A small bouncy fairy, with bright eyes and dark locks. She wears a simple dark blue dress that drapes around her shoulders."))
data["Quezlat's Hill"].add_character(Character("Jenqa", 10, False, "A shorter-than average Quezlat, with fine cheekbones and thin brown hair. He wears the traditional dark green robes for the People of the Earth."))
#DECLARE ADJACENCY HERE
data["Crossroads"].add_adj(data["Pond of Healing"])
data["Crossroads"].add_adj(data["Quezlat's Hill"])
data["Crossroads"].add_adj(data["Rainbow Stream of Knowledge"])
data["Crossroads"].add_adj(data["River of Lost"])

#PUT START LOCATION HERE
start = data["Clearing"]