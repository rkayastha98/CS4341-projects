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


        #minimax with alpha-beta pruning
        v=self.maxValue(brd,-100000,100000)
        # return the action in ACTIONS(state) with value v
        return actions(brd)


    def maxValue(state, alpha, beta):
        if terminalTest(state):
            return utility(state)
        value=-100000 #in place of -infinity
        for a in actions(state):
            value=max(value, minValue(result(S, a), alpha, beta))
            if value>=beta:
                return value
            alpha=max(alpha,value)
        return value

    def minValue(state, alpha, beta):
        if terminalTest(state):
            return utility(state)
        value = 100000 #in place of +infinity
        for a in actions(state):
            value = min(value, maxValue(result(S, a), alpha, beta))
            if value <= alpha:
                return value
            beta = min(alpha, value)
        return value
    
    #the next three functions are for checking the terminal state for both players
    def isLineAt(self, x, y, dx, dy):
        """ Return  True if a line of  identical  tokens  exists  starting  at (x,y)in  direction (dx ,dy)"""
        # Your  code  here
        num = self.board[x][y]
        count = 1
        for i in range(3):
            x = x+dx
            y = y+dy
            #Return 0 if out of bounds
            if(((x < 0) or (x >= self.w)) or ((y < 0) or (y >= self.h))):
                return 0
            #Keep count if the same non-zero number appears consecutively
            if(self.board[x][y] == num):
                count += 1
        #Check if the count is 4
        if ((count == 4) and (num != 0)):
            return num
        else:
            return 0
    
    def isAnyLineAt(self, x, y):
        """ Return  True if a line of  identical  symbols  exists  starting  at (x,y)in any  direction """
        return (self.isLineAt(x, y, 1, 0) or  # Horizontal
                self.isLineAt(x, y, 0, 1) or  # Vertical
                self.isLineAt(x, y, 1, 1) or  # Diagonal  up
                self.isLineAt(x, y, 1,  -1))  # Diagonal  down

    def terminalTest(self):
        """ Returns  the  winner  of the  game: 1 for  Player 1, 2 for  Player 2, and0 for no  winner """
        # check numbers throughout the board
        w=len(self.brd)
        h=len(self.brd[0])
        for x in range(self.w-2):
            for y in range(self.h-2):
                return self.isAnyLineAt(x, y)

        return false

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
            succ.append((nb,col))
        return succ


# THE_AGENT = AlphaBetaAgent("Group19", 4)

