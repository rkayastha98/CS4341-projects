# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')

# Import necessary stuff
import random
from game_stats import GameStats
from monsters.stupid_monster import StupidMonster

# sys.path.insert(1, '../groupNN')

# Create the game


# Run!
seedBegin = 1000
numGames = 100
wins = 0
for i in range(numGames):

    random.seed(seedBegin + i)
    g = GameStats.fromfile('scenario1/map.txt', "../bomberman/sprites/")
    g.add_monster(StupidMonster("stupid", "S", 3, 9))
    from expectimaxcharacter import ExpectimaxCharacter
    g.add_character(ExpectimaxCharacter("me", "C", 0, 0))
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

