# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import math
import utility

MAX_DEPTH = 2


class ExpectimaxCharacter(CharacterEntity):

    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.visited = dict()
        self.drop_bomb = False
    def do(self, wrld):
        # Your code here
        #get last monster
        monster_loc = [(wrld.monsters[monster][0].x, wrld.monsters[monster][0].y) for monster in wrld.monsters][-1]
        value, dest_cell = self.expectimax_last_monster_no_bombs(wrld, (self.x, self.y), monster_loc, None, True, 0)
        dx, dy = dest_cell
        self.set_cell_color(self.x + dx, self.y + dy, Back.RED)
        self.move(dx, dy)

        # self.visited[moveto] = self.visited.setdefault(moveto, 0) + 1

        pass

    def heuristic_last_monster_no_bombs(self, world, bman, monster, action):
        v = 0
        distance_to_monster = len(utility.a_star(bman, world, monster))#utility.distance(bman, monster)
        distance_to_exit = len(utility.a_star(bman, world, world.exitcell))#utility.distance(bman, world.exitcell)
        v += distance_to_monster
        v -= 2 * distance_to_exit
        if distance_to_monster < 2:
            v -= sys.maxsize
        return v, action

    def expectimax_last_monster_no_bombs(self, world, bman, monster, action, max_node, depth):
        value = 0
        taction = 0
        # Terminal Node
        if depth >= MAX_DEPTH:
            value, taction = self.heuristic2(world, bman, monster, action)
        # Max node
        elif max_node:
            children = utility.get_neighbors(world, bman)
            children.append(bman)
            successors = [self.expectimax_2(world, child, monster, (child[0] - bman[0], child[1] - bman[1]), False, depth + 1) for child in children]
            idx = max(range(len(successors)), key=lambda i: successors[i][0])
            value, taction = successors[idx]
        # Chance node
        else:
            children = utility.get_neighbors(world, monster)
            successors = [self.expectimax_2(world, bman, child, (child[0] - monster[0], child[1] - monster[1]), True, depth + 1)[0] for child in children]
            # idx = max(range(len(successors)), key=lambda i: successors[i][0])
            value = sum(successors) / len(successors)
            taction = action
        return value, taction