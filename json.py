import json
import random


class World:
    def __init__(self, n_players):
        self.n_players = n_players
        self.data = json.load(open('graph.json', 'r'))

    def print(self):
        print(json.dumps(random.choice(self.data[n_players - 1]['layouts']), indent=2))


n_players = 3
world = World(n_players)
world.print()
