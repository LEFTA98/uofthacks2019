from manager import Manager
from characters import Player
from gcp_nlp import Command
import json

if __name__ == "__main__":
#    json1_file = open('map.json')
#    json1_str = json1_file.read()
#    json1_data = json.loads(json1_str)
    
    data_file = open("map.py")
    data_str = data_file.read()
#    
    game_manager = Manager()
    
    #list of vars filled by exec
    data = None
    start = None
    exec(data_str)
    
    game_manager.hack_map(data, start)
    
    game_manager.player = Player()
    
    # only use this when not hacking 
    # game_manager.make_map(json1_data)
    
    print("""You wake up, badly bruised, freezing and with barely enough energy to move. 
Getting up, you look at your surroundings...""")
    
    #debug
    #print(game_manager.location.name)
    last_action = None
    
    while True:
        #enemies only attack after a non-inspect action
        if not (last_action is None or last_action.root == "inspect"):
            for character in game_manager.location.characters:
                if character.aggression and character.is_alive():
                    character.attack(game_manager.player)
                    
        if not game_manager.player.is_alive():
            print("You succumb to your injuries.")
            break 
        
        print(game_manager.location.description)
        print(game_manager.player.get_health_state())
        
        s = ""
        
        for char in game_manager.location.characters:
            if char.is_alive() and "hidden" not in char.status:
                s += "a " + char.name + ", "
        print("In the area you see the following living characters:")
        if s != "":
            print(s[:-2])

        s = ""
        
        for char in game_manager.location.characters:
            if (not char.is_alive()) and "hidden" not in char.status:
                s += "a " + char.name + ", "
        print("In the area you see the following dead characters:")
        if s != "":
            print(s[:-2])
                
        s = ""
        
        for item in game_manager.location.items:
            if "hidden" not in item.status:
                s += "a " + item.name + ", "
        print("In the area are the following items:")
        if s != "":
            print(s[:-2])
        command = input("What do you do? \n")
        
        command = game_manager.process(command)
        
        if command.root == 'take':
            for item in game_manager.location.items:
                if item.name == command.pobj:
                    game_manager.player.inventory.append(item)
                    game_manager.location.items.remove(item)
                    break
                
            print("You put the " + item.name + " into your bag.")
            
        elif command.root == 'inspect':
            for item in game_manager.location.items + game_manager.player.inventory:
                if item.name == command.pobj:
                    print(item.description)
                    
            for character in game_manager.characters:
                if character.name == command.pobj:
                    print(item.description)
                    
            if game_manager.location.name == command.pobj:
                print("Your current location is: " + command.pobj)
                print("Adjacent locations are: ")
                
                s = ''
                    
                for location in game_manager.location.adj:
                    s += "a " + item.name + ", "
                if s!= '':
                    print(s[:-2])
                    
        elif command.root == 'move':
            if game_manager.location.can_move():
                for zone in game_manager.location.adj:
                    if zone.name == command.pobj:
                        game_manager.location = zone
                        print("You move to the " + zone.name + ".")
            else:
                print("The enemies cut you off!")
                
        elif command.root == 'use':
            target = game_manager.player
            for character in game_manager.location.characters:
                if character.name == command.pobj:
                    target = character
                    
            for item in game_manager.player.inventory:
                if item.name == command.dobj:
                    prev_hp = target.health
                    item.on_use(target)
                    if target == game_manager.player:
                        print("You use the "+ item.name + " on yourself.")
                    else:
                        print("You use the "+ item.name + " on the "+ target.name + ".")
                        if prev_hp > 0 and not target.is_alive():
                            print("The target falls!")
                            
        elif command.root == "attack":
            target = None
            for character in game_manager.location.characters:
                if character.name == command.pobj:
                    target = character
                    
            for item in game_manager.location.items:
                if item.name == command.dobj:
                    prev_hp = target.health
                    item.on_use(target)
                    print("You strike the "+" target with your " + item.name + "!")
                    if prev_hp > 0 and not target.is_alive():
                            print("The target falls!")

        elif command.root == Command("move", None, "leaves") and game_manager.location.name == "Clearing":
            game_manager.getItem("body")
        elif command is None:
            print("Invalid action.")
            
        
        last_command = command
        print("\n")
