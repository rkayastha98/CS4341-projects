# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import math
import utility

MAX_DEPTH = 3


class ExpectimaxCharacter(CharacterEntity):

    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.visited = dict()
        self.drop_bomb = False
    def do(self, wrld):
        # Your code here
        # self.optimal_path = utility.a_star((self.x, self.y), wrld, wrld.exitcell)
        # for i in range(10):
        #     print(self.optimal_path[i])
        print(wrld.bombs)
        v, dest = self.expectimax_uniform(wrld, (self.x, self.y), True, 0)

        dx = dest[0] - self.x
        dy = dest[1] - self.y
        if(self.drop_bomb):
            self.place_bomb()
            self.drop_bomb = False

        self.set_cell_color(self.x + dx, self.y + dy, Back.RED)
        self.move(dx, dy)

        self.visited[dest] = self.visited.setdefault(dest, -2*utility.distance(wrld.exitcell, dest)) - 1

        pass

    def heuristic(self, wrld, state):
        x, y = state
        # x_goal, y_goal = wrld.exitcell
        # in_path = lambda a, alist: 1 if a in alist else 0
        if wrld.exit_at(x, y):
            return sys.maxsize
        elif wrld.monsters_at(x, y) is not None:
            monsters = utility.get_neighbors(wrld, state)
            return -(sys.maxsize - 1)

        else:
            if self.visited.setdefault(state, -2*utility.distance(wrld.exitcell, state)) < -50 / max(len(wrld.monsters), 1):
                self.drop_bomb = True
            monster_dist = 0
            if wrld.monsters:
                monster_dist = min([utility.distance(state, (wrld.monsters[monster][0].x, wrld.monsters[monster][0].y)) for monster in wrld.monsters])
            bomb_dist = 0
            if wrld.bombs:
                bomb_dist = min([utility.distance(state, (wrld.bombs[bomb].x, wrld.bombs[bomb].y)) for bomb in wrld.bombs])
            explosion_dist = 0
            if wrld.explosions:
                explosion_dist = min([utility.distance(state, (wrld.explosions[ex].x, wrld.explosions[ex].y)) for ex in wrld.explosions])
            if monster_dist > 5:
                monster_dist = 0
            return -2*utility.distance(wrld.exitcell, state) + self.visited[state] + (2*monster_dist**(len(wrld.monsters))) + (10*bomb_dist**len(wrld.bombs)) + (10*explosion_dist**len(wrld.explosions))
            #

            #return -1 * (abs(wrld.width() - x) + abs(wrld.height() - y))
        #     return -len(self.optimal_path) + (
        #                 self.distance_from_monster * 2) + 5 * in_path(state, self.optimal_path)
        # return 10 * in_path(state, self.optimal_path) - len(self.optimal_path)

    def expectimax_uniform(self, world, node, max_node, depth):

        # Condition for Terminal node
        if depth >= MAX_DEPTH:
            return self.heuristic(world, node)
        neighbors = utility.get_neighbors(world, node)
        # Max node
        if max_node:
            p = [self.expectimax_uniform(world, neighbor, False, depth + 1) for neighbor in neighbors]
            idx = max(range(len(p)), key=lambda i: p[i])
            print((depth * "   ") + "Depth %d -- Parent: (%d, %d) -- Value: %d" % (depth, node[0], node[1], max(p)))
            # print("DEPTH %d: Value %d at (%d, %d)" % (depth, max(p), neighbors[i][0], neighbors[i][1]))
            # print("DEPTH %d: Value %d at (%d, %d)" % (depth, max(p), neighbors[idx][0], neighbors[idx][1]))
            if depth == 0:
                # for i in range(len(p)):
                #     print("DEPTH %d: Value %d at (%d, %d)" % (depth, max(p), neighbors[i][0], neighbors[i][1]))
                return max(p), neighbors[idx]
            return max(p)

        # Chance node. Returns the average of
        # the left and right sub-trees
        else:
            return (sum([self.expectimax_uniform(world, neighbor, True, depth + 1) for neighbor in neighbors]) / len(
                neighbors))
