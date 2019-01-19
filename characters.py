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
    
class Character():
    
    def __init__(self, name, health, aggression):
        self.name = name
        self.max_health = health
        self.health = health
        self.aggression = aggression
        self.status = []
        self.inventory = []
        self.attacks = []
        self.responses = []
        
    def is_alive(self):
        return self.health > 0