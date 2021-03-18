# This is necessary to find the main code
import sys

from sensed_world import SensedWorld

sys.path.insert(0, '../bomberman')
# sys.path.insert(1, '../bomberman/monsters')
# Import necessary stuff
from entity import CharacterEntity
from events import *
from monsters.selfpreserving_monster import SelfPreservingMonster
from colorama import Fore, Back
import math
import utility

MAX_DEPTH = 3


class ExpectimaxCharacter(CharacterEntity):

    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        keylist = []
        # for i in range(w):
        #     for j in range(h):
        #         keylist.append((i, j))
        # self.visited = dict.fromkeys(keylist, 0)
        self.visited = dict()
        # self.drop_bomb = False
        self.num_monsters = 0

    def do(self, wrld):
        # Your code here
        value, dest_cell, drop_bomb, = self.expectimax_aggresive_monster_with_bombs(wrld, None, True, 0)
        # print("Value : %d, Destination : (%d, %d)" % (value, dest_cell[0], dest_cell[1]))
        dx = dest_cell[0] - self.x
        dy = dest_cell[1] - self.y
        self.set_cell_color(self.x + dx, self.y + dy, Back.RED)

        if drop_bomb:
            self.place_bomb()


        self.move(dx, dy)
        self.visited[dest_cell] = self.visited.setdefault(dest_cell, 0) + 1

    def heuristic_aggresive_monster_with_bombs(self, world, events):
        score = 0
        action = None
        bomb = False
        (nextworld, nextevents) = world.next()
        if nextevents is not None:
            nexttypes = [event.tpe for event in nextevents]
        if Event.BOMB_HIT_CHARACTER in nexttypes or Event.CHARACTER_KILLED_BY_MONSTER in nexttypes:
            return -(sys.maxsize - 1), action, bomb

        # elif Event.CHARACTER_FOUND_EXIT in types:
        #     return sys.maxsize, action, bomb


        # if BOMB_HIT_WALL in events:
        #     score += 10
        # if BOMB_HIT_MONSTER in events:
        #     score += 40
        # terminate if bomberman is dead (this should never trigger, should be handled in expectimax)


        #get all the entities
        bman = next(iter(world.characters.values()))[0]
        monsters = iter(world.monsters.values())
        bombs = iter(world.bombs.values())
        explosions = iter(world.explosions.values())

        # get the distance to the exit
        distance_to_exit = utility.grid_h((bman.x, bman.y), world.exitcell)#len(utility.a_star((bman.x, bman.y), world, world.exitcell))

        # incentivize approching exit - range on this should be between 0 and 45ish
        score -=  distance_to_exit
        # incentivize exploring new area
        score -= self.visited.setdefault((bman.x, bman.y), 0)
        for monster in monsters:
            sight_range = 1
            distance_to_monster = utility.grid_h((bman.x, bman.y), (monster[0].x, monster[0].y))#len(utility.a_star((bman.x, bman.y), world, (monster[0].x, monster[0].y)))
            # determine range based on type of monster
            if isinstance(monster[0], SelfPreservingMonster):
                sight_range = monster[0].rnge
            # we dont want monster to see us!
            if distance_to_monster <= sight_range:
                score -= 300
            # we want to reward killing monsters, by penalizing living monsters
            score -= 50
            for bomb in bombs:
                # score -= 7utility.grid_h(bomb[0].x, bomb[0].y, (monster[0].x, monster[0].y))
                #incentivize destroying walls
                score += 1
        score -= utility.get_wall_count(world)

        score += len(utility.get_neighbors(world, (bman.x, bman.y)))


        #     distance_to_bomb = utility.grid_h((bman.x, bman.y), world, (bomb.x, bomb.y)))#len(utility.a_star((bman.x, bman.y), world, (bomb.x, bomb.y)))
        #
        #     #bomb is about to explode and your in the blast zone!
        #     if bomb.timer == 1 and
        #         blast_zone = utility.get_blast_zone((bomb.x, bomb.y), world.expl_range)
        #
        #     if distance_to_bomb <= 1:
        #         score = -sys.maxsize
        # for explosion in explosions:
        #     distance_to_explosion = len(utility.a_star((bman.x, bman.y), world, (explosion.x, explosion.y)))
        #     if distance_to_explosion <= 1:
        #         score = -sys.maxsize


        # number_of_neighbors = len(utility.get_neighbors(world, (bman.x, bman.y)))
        # score += number_of_neighbors
        # v += distance_to_monster
        # v -= 2 * distance_to_exit
        # v += number_of_neighbors
        return score, action, bomb

    def expectimax_aggresive_monster_with_bombs(self, world, events, max_node, depth):
        score = 0
        action = None
        bomb = False
        types = []
        if events is not None:
            types = [event.tpe for event in events]
        if Event.BOMB_HIT_CHARACTER in types or Event.CHARACTER_KILLED_BY_MONSTER in types:
            score = -(sys.maxsize - 1)
        elif Event.CHARACTER_FOUND_EXIT in types:
            score = sys.maxsize
        # Terminal Node
        elif depth >= MAX_DEPTH:
            score, action, bomb = self.heuristic_aggresive_monster_with_bombs(world, events)
        # Max node
        elif max_node:
            tuples = []
            c = next(iter(world.characters.values()))[0]
            successors = utility.get_neighbors(world, (c.x, c.y))
            successors.append((c.x, c.y))
            for child in successors:
                potential_world = SensedWorld.from_world(world)
                c = next(iter(potential_world.characters.values()))[0]
                dx = child[0] - c.x
                dy = child[1] - c.y
                c.move(dx, dy)
                # (newwrld, events) = world.next()
                # tuples.append((self.expectimax_aggresive_monster_with_bombs(newwrld, events, False, depth + 1)[0], (child[0], child[1])))
                tuples.append((self.expectimax_aggresive_monster_with_bombs(potential_world, events, False, depth + 1)[0],
                               (child[0], child[1])))
            #Same thing but with BOMB
            for child in successors:
                potential_world = SensedWorld.from_world(world)
                c = next(iter(potential_world.characters.values()))[0]
                dx = child[0] - c.x
                dy = child[1] - c.y
                c.place_bomb()
                c.move(dx, dy)
                tuples.append((self.expectimax_aggresive_monster_with_bombs(potential_world, events, False, depth + 1)[0],
                               (child[0], child[1])))
            scores = [i[0] for i in tuples]

            score = max(scores)
            idx = max(range(len(scores)), key=lambda i: scores[i])

            action = tuples[idx][1]

            # for i in tuples:
            #     print("Action: (%d, %d), Value: %d, Visited: %d" % (i[1][0], i[1][1],  i[0], self.visited.get(i[1])))
            # if most valuable q node was in the second half of choices (we dropped a bomb before moving)
            if idx > len(tuples)/2:
                bomb = True
        # Chance node
        else:
            tuples = []
            if(len(world.monsters.values()) > 0):
                m = next(iter(world.monsters.values()))[0]
                for child in utility.get_neighbors(world, (m.x, m.y)):
                    potential_world = SensedWorld.from_world(world)
                    m = next(iter(potential_world.monsters.values()))[0]
                    # move monster to appropriate spot
                    m.move(child[0] - m.x, child[1] - m.y)
                    (newwrld, newevents) = potential_world.next()
                    tuples.append((self.expectimax_aggresive_monster_with_bombs(newwrld, newevents, True, depth + 1)[0], (child[0], child[1])))
            else:
                (world, events) = world.next()
                tuples.append((self.expectimax_aggresive_monster_with_bombs(world, events, True, depth + 1)[0], None))
            scores = [i[0] for i in tuples]
            # print(tuples)
            score = sum(scores) / len(scores)
        return score, action, bomb