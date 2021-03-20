# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import heapq
import math


class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        path = self.a_star((self.x, self.y), wrld)
        (dx, dy) = path.pop()
        self.set_cell_color(self.x+dx, self.y+dy, Back.RED)
        self.move(dx, dy)
        pass

    def a_star(self, start, wrld):
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

            # Check out every non-wall neighbor of current node
            for dx in [-1, 0, 1]:
                if (cx + dx >= 0) and (cx + dx < wrld.width()):
                    for dy in [-1, 0, 1]:
                        if (dx != 0) or (dy != 0):
                            if (cy + dy >= 0) and (cy + dy < wrld.height()):
                                if not wrld.wall_at(cx + dx, cy + dy):
                                    tentative_g_score = g_score[(cx, cy)] + 1
                                    if tentative_g_score < g_score.setdefault((cx + dx, cy + dy), math.inf):
                                        came_from[(cx + dx, cy + dy)] = (cx, cy)
                                        g_score[(cx + dx, cy + dy)] = tentative_g_score
                                        f_score[(cx + dx, cy + dy)] = g_score[(cx + dx, cy + dy)] + self.h(
                                            (cx + dx, cy + dy), wrld.exitcell)
                                        if not (cx + dx, cy + dy) in visit_list:
                                            heapq.heappush(to_visit, (f_score[(cx + dx, cy + dy)], (cx + dx, cy + dy)))
                                            visit_list.append((cx + dx, cy + dy))

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
