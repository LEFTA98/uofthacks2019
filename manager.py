from location import Location
from gcp_nlp import Command
from characters import Player
import gcp_nlp


class Manager():

    def __init__(self):
        """location: Location
            map: dictionary of location name to Location"""
        self.location = None
        self.world_map = None
        self.nlp_processor = None
        self.player = None

    def make_map(self, data):
        world_map = {}
        for location in data['locations'].keys():
            curr_loc = Location(
                location, data['locations'][location]["description"])

            for item in data['locations'][location]['items']:
                curr_loc.add_items(item)

        for location in data['adjacencies'].keys():
            curr_loc = world_map[location]
            for adjacent_location in data['adjacencies'][location]:
                curr_loc.add_adj(world_map[adjacent_location])

        self.world_map = world_map
        self.location = data['start']

    def hack_map(self, data, start):
        self.world_map = data
        self.location = start

    # nlpification happens here
    def process(self, input):
        return gcp_nlp.analyze(input, allowed_actions=self.get_valid_actions())

    def get_valid_actions(self):
        li_ = {}
        li_["inspect"] = {None: set()}
        
        for target in self.location.items + self.location.characters + [self.location] + self.player.inventory:
            li_.get("inspect", {}).get(None, set()).add(target.name)
            
        li_.get("inspect", {}).get(None, set()).add(None)

        li_["take"] = {None: set()}
        for target in self.location.items:
            li_.get("take", {}).get(None, set()).add(target.name)

        li_["move"] = {None: set()}
        for target in self.location.adj:
            li_.get("move", {}).get(None, set()).add(target.name)

        li_["attack"] = dict()
        for item in self.player.inventory:
            li_["attack"][item.name] = li_["attack"].get(item.name, set())
            if item.is_weapon:
                for target in self.location.characters:
                    li_.get("attack", {}).get(item.name, set()).add(target.name)

        li_["use"] = dict()
        for item in self.player.inventory:
            li_["use"][item.name] = set()
            for target in self.location.characters:
                li_.get("use", {}).get(item.name, set()).add(target.name)
            li_["use"][None] = set()
            li_.get("use", {}).get(None, set()).add(item.name)

        def add_itneract(a, b, c):
            li_[a] = li_.get(a, dict())
            li_[a][b] = li_[a].get(b, set())
            li_.get(a, {}).get(b, set()).add(c)
        # put any hardcoded iteractions here
        # FORMAT: add_interact("eat", "fork", "mushrooms") #### For something like Eat the mushrooms with a fork

        # self.location["Clearing"].

        return li_

    def getItem(self, name):
        for item in self.location.items:
            if item.name == name:
                return item
        return None


def get_and_add(dic, key, value):
    if key not in dic:
        dic[key] = {}
        return dic[key]
    else:
        return dic[key]
