from manager import Manager
from characters import Player
from gcp_nlp import Command
import json

if __name__ == "__main__":
    #    json1_file = open('map.json')
    #    json1_str = json1_file.read()
    #    json1_data = json.loads(json1_str)

    data_file = open("testmap.py")
    data_str = data_file.read()
#
    game_manager = Manager()

    # list of vars filled by exec
    data = None
    start = None
    exec(data_str)

    game_manager.hack_map(data, start)

    game_manager.player = Player()

    # only use this when not hacking
    # game_manager.make_map(json1_data)

    print("""You wake up, badly bruised, freezing and with barely enough energy to move. 
Getting up, you inspect your surroundings...""")

    # debug
    # print(game_manager.location.name)
    last_command = None

    while True:
        # enemies only attack after a non-inspect action
        if not (last_command is None or last_command.root == "inspect"):
            for character in game_manager.location.characters:
                if character.aggression and character.is_alive():
                    print(character.attack(game_manager.player))

        if not game_manager.player.is_alive():
            print("You succumb to your injuries.")
            break

        print(game_manager.location.description)
        print(game_manager.player.get_health_state())

        s = ""

        for char in game_manager.location.characters:
            if char.is_alive() and "hidden" not in char.status:
                s += char.name + ", "
        if s != "":
            print("In the area you see the following living characters:")
            print(s[:-2])

        s = ""

        for char in game_manager.location.characters:
            if (not char.is_alive()) and "hidden" not in char.status:
                s += char.name + ", "

        if s != "":
            print("In the area you see the following dead characters:")
            print(s[:-2])

        s = ""

        for item in game_manager.location.items:
            if "hidden" not in item.status:
                s += item.name + ", "
        print("In the area are the following items:")
        if s != "":
            print(s[:-2])
        command = input("What do you do? \n")
        
        if command.strip() == "break":
            exit()

        command = game_manager.process(command)
        # debug
#        print(game_manager.get_valid_actions())
#        print(command)
#        print(game_manager.player.health)

        if command is None:
            print("invalid action.")
        elif command.root == 'take':
            for item in game_manager.location.items:
                if item.name == command.pobj:
                    game_manager.player.inventory.append(item)
                    game_manager.location.items.remove(item)
                    break

            print("You put the " + item.name + " into your bag.")

        elif command.root == 'inspect':
            for item in game_manager.location.items + game_manager.player.inventory:
                if item.name == command.pobj or item.name == command.dobj:
                    print(item.description)

            for character in game_manager.location.characters:
                if character.name == command.pobj:
                    print(character.description)

            if game_manager.location.name == command.pobj or command.pobj is None:
                print("Your current location is: " +
                      game_manager.location.name)
                print("Adjacent locations are: ")

                s = ''

                for location in game_manager.location.adj:
                    s += location.name + ", "
                if s != '':
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
            for item in game_manager.player.inventory:
                if item.name == command.pobj:
                    item.on_use(target)
                    if item.name == "flask":
                        print("The liquid inside heals you!")
                    elif item.name == "mushrooms":
                        print(
                            "They taste a bit strange, but seem to have restorative properties.")
#            for character in game_manager.location.characters:
#                if character.name == command.pobj:
#                    target = character
#
#            for item in game_manager.player.inventory:
#                if item.name == command.dobj:
#                    prev_hp = target.health
#                    item.on_use(target)
#                    if target == game_manager.player:
#                        print("You use the "+ item.name + " on yourself.")
#                    else:
#                        print("You use the "+ item.name + " on the "+ target.name + ".")
#                        if prev_hp > 0 and not target.is_alive():
#                            print("The target falls!")

        elif command.root == "attack":
            target = None
            for character in game_manager.location.characters:
                if character.name == command.pobj:
                    target = character

            for item in game_manager.player.inventory:
                if item.name == command.dobj:
                    prev_hp = target.health
                    item.on_use(target)
                    print("You strike the "+" target with your " + item.name + "!")
                    if not target.aggression:
                        target.aggression = True
                        print("Your target has become aggressive!")
                    if prev_hp > 0 and not target.is_alive():
                        print("The target falls!")

        last_command = command
        print("\n")
