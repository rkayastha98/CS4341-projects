# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import heapq
import math


# returns a list of non-wall neighbors
def get_neighbors(wrld, node):
    x0, y0 = node
    neighbors = []
    for dx in [-1, 0, 1]:
        if (x0 + dx >= 0) and (x0 + dx < wrld.width()):
            for dy in [-1, 0, 1]:
                if (dx != 0) or (dy != 0):
                    if (y0 + dy >= 0) and (y0 + dy < wrld.height()):
                        if not wrld.wall_at(x0 + dx, y0 + dy):
                            neighbors.append((x0 + dx, y0 + dy))
    return neighbors

# returns a list of only wall neighbors
def get_wall_neighbors(wrld, node):
    x0, y0 = node
    neighbors = []
    for dx in [-1, 0, 1]:
        if (x0 + dx >= 0) and (x0 + dx < wrld.width()):
            for dy in [-1, 0, 1]:
                if (dx != 0) or (dy != 0):
                    if (y0 + dy >= 0) and (y0 + dy < wrld.height()):
                        if wrld.wall_at(x0 + dx, y0 + dy):
                            neighbors.append((x0 + dx, y0 + dy))
    return neighbors
def get_wall_count(wrld):
    count = 0
    for i in range(wrld.width()):
        for j in range(wrld.height()):
            if wrld.wall_at(i, j):
                count+=1
    return count


def a_star(start, wrld, dest):
    # Set of discovered nodes
    frontier = []
    heapq.heappush(frontier, (0, start))
    visited = [start]

    # Map for tracing previous node on shortest path
    came_from = dict()

    # Current cheapest known path from start to node n
    g_score = dict()
    g_score[start] = 0

    # f_score = g_score(n) + h(n)
    f_score = dict()
    f_score[start] = grid_h(start, dest)

    while frontier:
        current = heapq.heappop(frontier)[1]
        visited.remove(current)
        if current == dest:
            return reconstruct_path(came_from, start, current)
        neighbors = get_neighbors(wrld, current)
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.setdefault(neighbor, math.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + grid_h(neighbor, wrld.exitcell)
                if neighbor not in visited:
                    heapq.heappush(frontier, (f_score[neighbor], neighbor))
                    visited.append(neighbor)


def grid_h(node, goal):
    dx = abs(node[0] - goal[0])
    dy = abs(node[1] - goal[1])
    return dx + dy


def reconstruct_path(came_from, start, end):
    path = []
    current = end
    while not current == start:
        last_node = came_from[current]
        path.append((current[0] - last_node[0], current[1] - last_node[1]))
        current = last_node
    return path


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2+(y2 - y1)**2)

def get_blast_zone(bomb_loc, radius):
    return [[(bomb_loc[0] + delta * axis, bomb_loc[1] + delta * (1-axis)) for axis in [0, 1]] for delta in range(-radius, 0) + range(1, radius+1)]