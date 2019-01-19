from characters import Character
from item import Item

class Location():
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.adj = []
        self.characters = []
        self.items = []
        
    def add_adj(self, location):
        self.adj.append(location)
        
    def add_character(self, character):
        self.characters.append(character)
        
    def add_item(self, item):
        self.items.append(item)