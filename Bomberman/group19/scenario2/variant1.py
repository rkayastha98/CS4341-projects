# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../group19')
from testcharacter import TestCharacter


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
from expectimaxcharacter import ExpectimaxCharacter
g.add_character(ExpectimaxCharacter("me", "C", 0, 0, 25, 1, 100, 1))

# Run!
g.go(1)
