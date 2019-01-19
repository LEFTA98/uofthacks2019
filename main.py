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
    print(game_manager.location.name)
    
    while True:
        print(game_manager.location.description)
        print(game_manager.player.get_health_state())
        command = input("What do you do? \n")
        