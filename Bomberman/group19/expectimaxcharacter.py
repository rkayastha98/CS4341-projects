# This is necessary to find the main code
import sys

from sensed_world import SensedWorld

sys.path.insert(0, '../bomberman')
# sys.path.insert(1, '../bomberman/monsters')
# Import necessary stuff
from entity import CharacterEntity
from events import *
from monsters.selfpreserving_monster import SelfPreservingMonster
from monsters.stupid_monster import StupidMonster
from colorama import Fore, Back
import math
import utility
from smart_monster import SmartMonster

MAX_DEPTH = 3


class ExpectimaxCharacter(CharacterEntity):

    def __init__(self, name, avatar, x, y, urgency, curiosity, monsterfear, claustrophobia):
        CharacterEntity.__init__(self, name, avatar, x, y)
        keylist = []
        # for i in range(w):
        #     for j in range(h):
        #         keylist.append((i, j))
        # self.visited = dict.fromkeys(keylist, 0)
        self.visited = dict()
        # self.drop_bomb = False
        self.num_monsters = 0
        # For all of these weights, A higher value idicates a larger penalty
        # Weight for the penalty for being far from exit
        self.weight_exit_distance = urgency
        # Weight for the penalty applied for revisiting a node
        self.weight_visited = curiosity
        # Weight for the penalty applied for a monster seeing bomberman
        self.weight_monster_fear = monsterfear
        # Weight for the penalty applied for each walled off neighbor
        self.weight_claustrophobia = claustrophobia

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
        # explosions = iter(world.explosions.values())

        score -= self.weight_claustrophobia * (8 - len(utility.get_neighbors(world, (bman.x, bman.y)))) / 8
        distance_normalize = utility.manhattan_distance((0, 0), world.exitcell)

        # get the normalized distance to the exit
        a_star = utility.a_star((bman.x, bman.y), world, world.exitcell)
        if a_star is not None:
            distance_to_exit = len(a_star) / distance_normalize
        else:
            distance_to_exit = utility.manhattan_distance((bman.x, bman.y), world.exitcell) / distance_normalize


        # incentivize approching exit - range on this should be between 0 and 45ish
        score -= self.weight_exit_distance * distance_to_exit
        # incentivize exploring new area
        score -= self.weight_visited * self.visited.setdefault((bman.x, bman.y), 0)
        for monster in monsters:
            sight_range = 1
            a_star_monster = utility.a_star((bman.x, bman.y), world, (monster[0].x, monster[0].y))
            if a_star_monster is not None:
                distance_to_monster = len(a_star_monster) / distance_normalize
            else:
                distance_to_monster = utility.manhattan_distance((bman.x, bman.y), (monster[0].x, monster[0].y)) / distance_normalize
            normalized_distance_to_monster = distance_to_monster / distance_normalize

            # determine range based on type of monster
            if monster[0].name == "selfpreserving":
                sight_range = 1
            if monster[0].name == "aggressive":
                sight_range = 2
            # we dont want monster to see us!
            if distance_to_monster <= sight_range:
                score -= self.weight_monster_fear * sight_range
                score += self.weight_monster_fear * normalized_distance_to_monster
            # we want to reward killing monsters, by penalizing living monsters
            score -= 50
        for bomb in bombs:
            # score -= 7utility.grid_h(bomb[0].x, bomb[0].y, (monster[0].x, monster[0].y))
            #incentivize destroying walls
            score += 1
        # score -= utility.get_wall_count(world)




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
            # if depth == 0:
            #     for i in tuples:
            #         print("Action: (%d, %d), Value: %d" % (i[1][0], i[1][1],  i[0]))
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
            sum = 0
            n = 0
            if len(world.monsters.values()) > 0:
                m = next(iter(world.monsters.values()))[0]
                if m.name == "stupid":
                    for child in utility.get_neighbors(world, (m.x, m.y)):
                        potential_world = SensedWorld.from_world(world)
                        mp = next(iter(potential_world.monsters.values()))[0]
                        mp.move(child[0] - mp.x, child[1] - mp.y)
                        (newwrld, newevents) = potential_world.next()
                        sum += self.expectimax_aggresive_monster_with_bombs(newwrld, newevents, True, depth + 1)[0]
                        n += 1

                elif m.name == "selfpreserving" or m.name == "aggressive":
                    temp_monster = SmartMonster(m, 2)
                    actions = temp_monster.get_actions(world)
                    for action in actions:
                        potential_world = SensedWorld.from_world(world)
                        mp = next(iter(potential_world.monsters.values()))[0]
                        mp.move(action[0], action[1])
                        (newwrld, newevents) = potential_world.next()
                        sum += self.expectimax_aggresive_monster_with_bombs(newwrld, newevents, True, depth + 1)[0]
                        n += 1
                score = sum / max(n, 1)
            else:
                (newwrld, newevents) = world.next()
                score = self.expectimax_aggresive_monster_with_bombs(newwrld, newevents, True, depth + 1)[0]

        return score, action, bomb

