# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(3, '../groupNN')

# Create the game
random.seed(1087) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 9      # position
))

# TODO Add your character
from expectimaxcharacter import ExpectimaxCharacter
g.add_character(ExpectimaxCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))
print(g.world.bomb_time)
# Run!
g.go(100)
