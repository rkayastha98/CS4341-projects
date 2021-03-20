# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')

# Import necessary stuff
import random
from game_stats import GameStats
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster
from expectimaxcharacter import ExpectimaxCharacter
# sys.path.insert(1, '../group19')

# Create the game


# Run!
seedBegin = 1000
numGames = 100
wins = 0
for i in range(numGames):

    random.seed(seedBegin + i)
    g = GameStats.fromfile('scenario2/map.txt', "../bomberman/sprites/")
    # g.add_monster(StupidMonster("stupid", "S", 3, 5))
    g.add_monster(SelfPreservingMonster("selfpreserving", "S", 3, 9, 1))
    # g.add_monster(SelfPreservingMonster("aggressive", "A", 3, 13, 2))
    g.add_character(ExpectimaxCharacter("me", "C", 0, 0, 25, 1, 2000, 1))


    lastwins = wins
    wins += g.go(0)
    if not wins > lastwins:
        print("Game #%d lost" % i)
    else:
        print("Game #%d won" % i)
print("Simulated %d games." % numGames)
print("Wins = %d" % wins)
print("Losses = %d" % (numGames - wins))
print("Player won %f of the time." % (wins / numGames * 100))

