class Item():
    
    def __init__(self, name, description, consumable, is_weapon, on_use, on_pickup):
        self.name = name
        self.description = description
        self.consumable = consumable
        self.is_weapon = is_weapon
        self.on_use = on_use
        self.on_pickup = on_pickup
        self.status = []