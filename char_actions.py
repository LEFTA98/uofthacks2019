class Action():
    
    def __init__(self, trigger, text):
        self.trigger = trigger
        self.text = ""
        
    def check_trigger(self, input_tag):
        return input_tag == self.trigger
            
class Attack():
    """this is for enemy attacks only!"""
    
    def __init__(self, damage, text):
        self.damage = damage
        self.text = text
    