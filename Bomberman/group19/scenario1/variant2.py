# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster

# This is your code!
sys.path.insert(3, '../group19')
from expectimaxcharacter import ExpectimaxCharacter

# Create the game
random.seed(123) # Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(StupidMonster("stupid", # name
                            "S",      # avatar
                            3, 9      # position
))

# TODO Add your character

g.add_character(ExpectimaxCharacter("me", "C", 0, 0, 25, 1, 100, 1))
# Run!
g.go(1)
