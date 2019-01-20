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
        for target in self.location.items + self.location.characters + [self.location.name]:
            li_.get("inspect", {}).get(None, set()).add(target)

        for target in self.location.items:
            li_.get("take", {}).get(None, set()).add(target)

        for target in self.location.adj:
            li_.get("move", {}).get(None, set()).add(target)

        for item in self.location.items:
            if item.is_weapon:
                for target in self.location.characters:
                    li_.get("attack", {}).get(item, set()).add(target)

        for item in self.location.items:
            for target in self.location.characters + [None]:
                li_.get("use", {}).get(item, set()).add(target)

        def add_itneract(a, b, c):
            li_.get(a, {}).get(b, set()).add(c)
        # put any hardcoded iteractions here
        # FORMAT: add_interact("eat", "fork", "mushrooms") #### For something like Eat the mushrooms with a fork

        return li_
