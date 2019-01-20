from char_actions import Attack
from char_actions import Action
from item import Item

class Player():

    def __init__(self):
        self.max_health = 10
        self.health = 4
        self.status = []
        self.inventory = []

    def is_alive(self):
        return self.health > 0

    def get_health_state(self):
        if self.health == self.max_health:
            return "You feel healthy."
        elif self.health >= 2/3 * self.max_health:
            return "You are lightly injured."
        elif self.health >= 1/3 * self.max_health:
            return "You are moderately injured."
        else:
            return "You are grievously injured."
        
    def has_weapon(self):
        for item in self.inventory:
            if item.is_weapon:
                return True
        return False

    def pickup(self, item):
        self.inventory.append(item)
        item.on_pickup()

    def use(self, item, target):
        item.on_use(target)
        if item.consumable:
            self.inventory.remove(item)


class Character():

    def __init__(self, name, health, aggression, description, response=None):
        self.name = name
        self.max_health = health
        self.health = health
        self.aggression = aggression
        self.description = description
        self.status = []
        self.inventory = []
        self.attacks = []
        self.response = response

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        if len(self.attacks) == 0:
            return ""
        else:
            chosen_attack = self.attacks[0]

            if target.is_alive():
                target.health -= chosen_attack.damage
            return chosen_attack.text
                
    def add_attack(self, attack_to_add):
        self.attacks.append(attack_to_add)

    def respond(self):
        print(self.response)
