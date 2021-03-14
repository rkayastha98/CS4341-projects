# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import heapq
import math


class Variant2Character(CharacterEntity):

    def do(self, wrld):
        # Your code here
        path = self.a_star_modified((self.x, self.y), wrld)
        if not path is None:
            (dx, dy) = path.pop()
            self.set_cell_color(self.x + dx, self.y + dy, Back.LIGHTGREEN_EX)
            self.move(dx, dy)
        else:
            self.move(0, 0)
        pass

    #returns a list of non-wall surroundings
    def get_surroundings(self, wrld, x0, y0):

        surroundings = []
        for dx in [-1, 0, 1]:
            if (x0 + dx >= 0) and (x0 + dx < wrld.width()):
                for dy in [-1, 0, 1]:
                    if (dx != 0) or (dy != 0):
                        if (y0 + dy >= 0) and (y0 + dy < wrld.height()):
                            if not wrld.wall_at(x0 + dx, y0 + dy):
                                surroundings.append((x0 + dx, y0 + dy))

        return surroundings

    def a_star_modified(self, start, wrld):
        # Set of discovered nodes
        to_visit = []
        heapq.heappush(to_visit, (0, start))
        visit_list = [start]

        # Map for tracing previous node on shortest path
        came_from = dict()

        # Current cheapest known path from start to node n
        g_score = dict()
        g_score[start] = 0

        # f_score = g_score(n) + h(n)
        f_score = dict()
        f_score[start] = self.h(start, wrld.exitcell)

        while to_visit:
            (cx, cy) = heapq.heappop(to_visit)[1]
            visit_list.remove((cx, cy))
            if (cx, cy) == wrld.exitcell:
                return self.reconstruct_path(came_from, (self.x, self.y), (cx, cy))
            neighbors = self.get_surroundings(wrld, cx, cy)
            # Check out every non-wall neighbor of current node
            for neighbor in neighbors:
                xn, yn = neighbor
                monster_flag = 0
                if wrld.monsters_at(xn, yn) is None:
                    second_neighbors = self.get_surroundings(wrld, xn, yn)
                    for second_neighbor in second_neighbors:
                        xn2, yn2 = second_neighbor
                        if not wrld.monsters_at(xn2, yn2) is None:
                            self.set_cell_color(xn2, yn2, Back.RED)
                            monster_flag += 1

                    if monster_flag == 0:

                        tentative_g_score = g_score[(cx, cy)] + 1
                        if tentative_g_score < g_score.setdefault((xn, yn), math.inf):
                            came_from[(xn, yn)] = (cx, cy)
                            g_score[(xn, yn)] = tentative_g_score
                            f_score[(xn, yn)] = g_score[(xn, yn)] + self.h(
                                (xn, yn), wrld.exitcell)
                            if not (xn, yn) in visit_list:
                                heapq.heappush(to_visit, (f_score[(xn, yn)], (xn, yn)))
                                visit_list.append((xn, yn))

    def reconstruct_path(self, came_from, start, end):
        path = []

        current = end
        while not current == start:
            last_node = came_from[current]
            path.append((current[0] - last_node[0], current[1] - last_node[1]))
            current = last_node
        return path

    def h(self, node, goal):
        dx = abs(node[0] - goal[0])
        dy = abs(node[1] - goal[1])
        return dx + dy
