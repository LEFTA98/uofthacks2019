from manager import Manager
from characters import Player
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
    
    while True:
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
        print("\n")
