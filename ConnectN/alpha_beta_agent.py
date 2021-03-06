import math
import agent


###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        (value, col) = self.minmax_value(brd, -1, -math.inf, math.inf, 0, True)
        return col

    # Maximize or minimize value of next move
    #
    # PARAM
    # RETURN [(int, int)] : tuple with the best possible value and the
    #                       corresponding move choice
    def minmax_value(self, state, col, alpha, beta, level, maximize):
        if level >= self.max_depth:
            return (self.heuristic(state, col, maximize), col)

        # -inf if max level, +inf if min level
        value = -math.inf if maximize else math.inf
        bestCol = -1
        # test each column choice
        for (child_state, child_col) in self.get_successors(state):
            if maximize:
                # MAX_VALUE option
                v, b = self.minmax_value(child_state, child_col, alpha, beta, level + 1, False)
                value = max(value, v)
                if value > alpha:
                    alpha = value
                    bestCol = child_col
            else:
                # MIN_VALUE option
                v, b = self.minmax_value(child_state, child_col, alpha, beta, level + 1, True)
                value = min(value, v)
                if value < beta:
                    beta = value
                    bestCol = child_col

            # check pruning condition
            if alpha >= beta:
                return value, bestCol

        return value, bestCol

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb, col))
        return succ

    def distance_from_center(self, col, brd):
        return abs(col - (int(brd.w / 2)))

    def get_list_of_lines(self, brd, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        lines = []
        blacklist = {}
        for y in range(brd.h):
            for x in range(brd.w):
                if (brd.board[y][x] != player):
                    continue
                for dir in directions:
                    j = y
                    i = x
                    l = 0
                    # print("\tLooking in direction X=%d Y=%d" % (dir[0], dir[1]))
                    for k in range(2, brd.n):
                        i += dir[0]
                        j += dir[1]
                        if (i < brd.w and i >= 0 and j < brd.h and j >= 0) and (
                                brd.board[j][i] == player):  # if correct player and in bounds
                            if not (j, i) in blacklist:
                                blacklist[(j, i)] = []
                            if dir in blacklist[(j, i)]:
                                break
                            blacklist[(j, i)].append(dir)
                            l = k
                            # print("\t\t%d" % l)
                        else:
                            break
                    if (l > 1):
                        lines.append(l)  # save line
                    # print("Path of length %d found from (%d, %d) to (%d, %d)" % (l, x, y, i, j))
        return lines

    def heuristic(self, state, col, maximize):
        # initialize result value
        result = 0

        # check board for 1, 2, or 3-in a row formations (4 if connect 5)
        # exponential increase in value for longer lines
        lines_agt = self.get_list_of_lines(state, self.player)
        lines_opp = self.get_list_of_lines(state, (self.player % 2) + 1)
        line_weight_agt = 0
        line_weight_opp = 0

        for x in range(2, state.n):
            weight = 3 ** (x - 1)
            line_weight_agt += lines_agt.count(x) * weight
            line_weight_opp += lines_opp.count(x) * weight

        result += line_weight_agt - line_weight_opp if maximize else line_weight_opp - line_weight_agt

        # favor plays towards the center of the board - low weight
        #if maximize:
        result += 100 / ((self.distance_from_center(col, state) + 1) ** 2)
        #else:
         #   result -= 100 / ((self.distance_from_center(col, state) + 1) ** 2)

        # backup win/loss check - heavily weighted
        # 1 for Player 1, 2 for Player 2, 0 for neither
        end_check = state.get_outcome()
        if end_check == 0:
            return result

        if (end_check == self.player):  # or (not maximize and end_check == (self.player + 1) % 2):
            result += 100000
        else:
            result += -100000

        return result


THE_AGENT = AlphaBetaAgent("Group19Agent", 5)
